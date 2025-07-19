import React, { useState } from 'react';
import FileUploader from "./FileUploader";
const ExtractionTabs = () => {
  const [activeTab, setActiveTab] = useState('tesseract');

  const tabClass = (tab) =>
    `px-6 py-2 text-sm font-semibold rounded-t-lg transition duration-200 ${
      activeTab === tab
        ? 'bg-red-600 text-white shadow-md'
        : 'text-red-600 border-b-2 border-transparent hover:border-red-600'
    }`;

  return (
    <div className="bg-white rounded-md shadow-sm max-w-3xl mx-auto mt-10">

      <div className="flex space-x-4 border-b border-gray-200 px-4 pt-4">
        <button className={tabClass('tesseract')} onClick={() => setActiveTab('tesseract')}>
          Tesseract
        </button>
        <button className={tabClass('llm')} onClick={() => setActiveTab('llm')}>
          LLM (Recommended)
        </button>
      </div>

      {/* Tab Content */}
      <div className="p-6">
        <FileUploader type={activeTab}/>
      </div>
    </div>
  );
};

export default ExtractionTabs;
