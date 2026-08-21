// components/Results.jsx
export default function Results({ data, onReset }) {
  return (
    <div className="animate-fade-in-up">
      <div className="flex justify-between items-center mb-6 border-b pb-4">
        <h2 className="text-2xl font-bold text-gray-800">Results Dashboard</h2>
        <button onClick={onReset} className="text-sm text-blue-600 hover:underline">
          ← Upload New File
        </button>
      </div>

      <div className="bg-blue-50 rounded-lg p-6 mb-6 border border-blue-100">
        <h3 className="text-lg font-bold text-blue-900 mb-2">📝 Executive Summary</h3>
        <p className="text-blue-800">{data.summary}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-green-50 rounded-lg p-6 border border-green-100">
          <h3 className="text-lg font-bold text-green-900 mb-4">✅ Action Items</h3>
          <ul className="space-y-2">
            {data.actionItems.map((item, i) => (
              <li key={i} className="flex items-start">
                <span className="text-green-500 mr-2">➜</span>
                <span className="text-green-800">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-purple-50 rounded-lg p-6 border border-purple-100">
          <h3 className="text-lg font-bold text-purple-900 mb-4">🎯 Key Decisions</h3>
          <ul className="list-disc pl-5 space-y-2">
            {data.decisions.map((decision, i) => (
              <li key={i} className="text-purple-800">{decision}</li>
            ))}
          </ul>
        </div>
      </div>

      <details className="bg-gray-50 rounded-lg border border-gray-200 cursor-pointer group">
        <summary className="p-4 font-semibold text-gray-700 outline-none">
          📄 View Full Transcript
        </summary>
        <div className="p-4 border-t border-gray-200 text-gray-600 whitespace-pre-wrap font-mono text-sm">
          {data.transcript}
        </div>
      </details>
    </div>
  );
}