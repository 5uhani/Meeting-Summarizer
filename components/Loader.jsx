// components/Loader.jsx
export default function Loader() {
  return (
    <div className="flex flex-col items-center justify-center py-20 animate-pulse">
      <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-6"></div>
      <h2 className="text-2xl font-bold text-gray-700">Analyzing Meeting...</h2>
      <p className="text-gray-500 mt-2">Transcribing audio and extracting action items.</p>
    </div>
  );
}