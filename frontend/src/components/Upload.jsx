import { useRef } from "react";
import { Plus, Loader2 } from "lucide-react";
import "./Upload.css";

const ACCEPTED_TYPES =
  ".pdf,.doc,.docx,.xlsx,.xls,.csv,.pptx,.ppt,.txt,.md,.png,.jpg,.jpeg,.mp3,.wav,.mp4,.avi,.mov";

export default function Upload({ onFileSelect, disabled, uploading }) {
  const fileRef = useRef(null);

  const handleClick = () => {
    if (disabled || uploading) return;
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
        className={`upload-btn ${uploading ? "upload-btn--loading" : ""}`}
        onClick={handleClick}
        disabled={disabled || uploading}
        aria-label={uploading ? "Uploading file" : "Attach file"}
      >
        {uploading ? (
          <Loader2 size={22} strokeWidth={1.75} className="upload-btn__spinner" />
        ) : (
          <Plus size={22} strokeWidth={1.75} />
        )}
      </button>
      <input
        ref={fileRef}
        type="file"
        accept={ACCEPTED_TYPES}
        hidden
        onChange={handleChange}
      />
    </>
  );
}
