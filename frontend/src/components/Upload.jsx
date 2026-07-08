import { useRef } from "react";
import { Plus } from "lucide-react";
import "./Upload.css";

export default function Upload({ onFileSelect }) {
  const fileRef = useRef(null);

  const handleClick = () => {
    fileRef.current?.click();
  };

  const handleChange = (e) => {
    const file = e.target.files?.[0];
    if (file && onFileSelect) {
      onFileSelect(file);
    }
    e.target.value = "";
  };

  return (
    <>
      <button
        type="button"
        className="upload-btn"
        onClick={handleClick}
        aria-label="Attach file"
      >
        <Plus size={22} strokeWidth={1.75} />
      </button>
      <input
        ref={fileRef}
        type="file"
        accept=".pdf,.doc,.docx,.txt"
        hidden
        onChange={handleChange}
      />
    </>
  );
}
