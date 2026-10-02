"use client";

import { useEffect, useRef, useState } from "react";

const initialMessages = [
  { role: "assistant", content: "Nexa Mind is ready. Upload an image or ask what you are looking at." },
];

export default function HomePage() {
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState("");
  const [status, setStatus] = useState("Idle");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const videoRef = useRef<HTMLVideoElement | null>(null);

  useEffect(() => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) return;

    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      })
      .catch(() => {
        setStatus("Camera unavailable; upload an image instead.");
      });
  }, []);

  useEffect(() => {
    if (!selectedFile) {
      setPreviewUrl(null);
      return;
    }

    const objectUrl = URL.createObjectURL(selectedFile);
    setPreviewUrl(objectUrl);
    return () => URL.revokeObjectURL(objectUrl);
  }, [selectedFile]);

  const sendMessage = async () => {
    if (!input.trim() && !selectedFile) return;

    const newMessage = {
      role: "user",
      content: input || "Analyze this image",
    };
    setMessages((prev) => [...prev, newMessage]);
    setStatus("Analyzing image...");
    setInput("");

    try {
      let responseText = "I’m processing your request.";

      if (selectedFile) {
        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("prompt", input || "What is this?");

        const uploadResponse = await fetch("http://localhost:8000/api/images/analyze", {
          method: "POST",
          body: formData,
          headers: {
            Authorization: `Bearer ${localStorage.getItem("nexa_token") || ""}`,
          },
        });

        const uploadData = await uploadResponse.json();
        responseText = `Image analysis: ${uploadData.analysis?.label || "Object"}. ${uploadData.analysis?.description || ""}`;
      } else {
        const result = await fetch("http://localhost:8000/api/chat/message", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("nexa_token") || ""}`,
          },
          body: JSON.stringify({ content: input }),
        });

        const data = await result.json();
        responseText = data.response || "No answer available.";
      }

      setMessages((prev) => [...prev, { role: "assistant", content: responseText }]);
      setStatus("Response ready");
    } catch (error) {
      setMessages((prev) => [...prev, { role: "assistant", content: "I could not complete the request. Please check the backend connection." }]);
      setStatus("Error");
    }
  };

  const loginDemo = async () => {
    const email = "demo@nexamind.ai";
    const password = "demo1234";

    const response = await fetch("http://localhost:8000/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (response.status === 400) {
      const loginResponse = await fetch("http://localhost:8000/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const loginData = await loginResponse.json();
      localStorage.setItem("nexa_token", loginData.access_token || "");
      setStatus("Authenticated");
      return;
    }

    const tokenData = await response.json();
    if (tokenData && tokenData.access_token) {
      localStorage.setItem("nexa_token", tokenData.access_token);
      setStatus("Authenticated");
    }
  };

  return (
    <main className="page-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">N</div>
          <div>
            <h1>Nexa Mind</h1>
            <p>Vision + Retrieval AI</p>
          </div>
        </div>

        <div className="status-card">
          <span className="status-dot" />
          {status}
        </div>

        <div className="panel-card">
          <h3>Camera</h3>
          <div className="camera-box">
            <video ref={videoRef} autoPlay playsInline muted />
          </div>
          <button className="secondary" onClick={loginDemo}>Authenticate demo user</button>
        </div>

        <div className="panel-card">
          <h3>Context</h3>
          <ul className="context-list">
            <li>Detected object: unknown</li>
            <li>Knowledge source: memory + web</li>
            <li>Retrieval status: live</li>
          </ul>
        </div>
      </aside>

      <section className="main-panel">
        <header className="topbar">
          <div>
            <p className="eyebrow">AI perception assistant</p>
            <h2>Live perception workspace</h2>
          </div>
          <button className="primary" onClick={loginDemo}>Demo login</button>
        </header>

        <div className="workspace-grid">
          <div className="chat-card">
            <div className="chat-body">
              {messages.map((message, idx) => (
                <div key={idx} className={`bubble ${message.role}`}>
                  {message.content}
                </div>
              ))}
            </div>

            <div className="composer">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask what you are looking at..."
              />
              <label className="upload-btn">
                Upload image
                <input type="file" accept="image/*" onChange={(e) => setSelectedFile(e.target.files?.[0] || null)} />
              </label>
              <button className="primary" onClick={sendMessage}>Send</button>
            </div>
          </div>

          <div className="inspector-card">
            <h3>Visual context</h3>
            {previewUrl ? (
              <img src={previewUrl} alt="Upload preview" className="preview-image" />
            ) : (
              <div className="placeholder-box">No image selected yet</div>
            )}

            <div className="source-list">
              <div className="source-item">
                <span>Image</span>
                <strong>Camera or upload</strong>
              </div>
              <div className="source-item">
                <span>Document KB</span>
                <strong>Indexed</strong>
              </div>
              <div className="source-item">
                <span>Web</span>
                <strong>Available</strong>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
