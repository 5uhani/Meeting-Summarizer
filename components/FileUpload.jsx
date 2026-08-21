// components/FileUpload.jsx
export default function FileUpload({ onUpload }) {
  const handleDragOver = (e) => e.preventDefault();
  
  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onUpload(e.dataTransfer.files[0]);
    }
  };

  return (
    <div 
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      className="border-4 border-dashed border-blue-200 rounded-xl p-12 flex flex-col items-center justify-center text-center cursor-pointer transition-all duration-300 hover:border-blue-500 hover:bg-blue-50 hover:scale-[1.02] group"
    >
      <div className="text-6xl mb-4 group-hover:animate-bounce">📁</div>
      <p className="text-xl font-semibold text-gray-700">Drag & drop your audio file here</p>
      <p className="text-gray-500 mt-2">or click to browse files</p>
      <p className="text-sm text-gray-400 mt-4">(Supported: .wav, .mp3, .m4a)</p>
      
      <input 
        type="file" 
        className="hidden" 
        accept="audio/*" 
        onChange={(e) => onUpload(e.target.files[0])}
        id="fileInput"
      />
      <button 
        onClick={() => document.getElementById('fileInput').click()}
        className="mt-6 px-6 py-3 bg-blue-600 text-white font-bold rounded-lg shadow-lg hover:bg-blue-700 hover:shadow-xl transition-all"
      >
        Browse Files
      </button>
    </div>
  );
}