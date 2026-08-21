// App.jsx
import { useState } from 'react';
import FileUpload from './components/FileUpload';
import Loader from './components/Loader';
import Results from './components/Results';

export default function App() {
  const [appState, setAppState] = useState('upload'); // 'upload', 'loading', 'results'
  const [summaryData, setSummaryData] = useState(null);

  const handleFileUpload = async (file) => {
    setAppState('loading');
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/summarize', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error("Failed to process audio");

      const data = await response.json();
      
      // Update state with the data from Python
      setSummaryData({
        summary: data.summary,
        decisions: data.decisions,
        actionItems: data.actionItems,
        transcript: data.transcript
      });
      setAppState('results');
      
    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong analyzing the meeting.");
      resetApp();
    }
  };

  const resetApp = () => {
    setSummaryData(null);
    setAppState('upload');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-12 px-4">
      <div className="w-full max-w-4xl bg-white rounded-2xl shadow-xl overflow-hidden p-8 transition-all duration-500">
        <h1 className="text-3xl font-bold text-gray-800 text-center mb-8">
          🎙️ Meeting Summarizer
        </h1>

        {appState === 'upload' && <FileUpload onUpload={handleFileUpload} />}
        {appState === 'loading' && <Loader />}
        {appState === 'results' && <Results data={summaryData} onReset={resetApp} />}
      </div>
    </div>
  );
}