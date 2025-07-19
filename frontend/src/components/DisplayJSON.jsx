



const DisplayJSON = ({data}) => {
    function handleDownload() {
    const jsonStr = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'extracted_data.json';
    a.click();
    URL.revokeObjectURL(url);
    }
    return (
        <>
        <div className="bg-gray-900 text-gray-100 rounded-xl overflow-hidden shadow-lg max-w-3xl mx-auto">
            <div className="bg-red-600 text-xs uppercase px-4 py-2 font-bold tracking-wide text-white">
                json
            </div>
            <pre className="text-sm p-4 overflow-x-auto whitespace-pre-wrap break-words">
                <code className="language-json">
                    {JSON.stringify(data)}
                </code>
            </pre>
        </div>

    <div className="px-4 py-3 flex ">
        <button
            onClick={handleDownload}
            className="bg-red-600 text-white font-semibold px-6 py-2 rounded-md hover:bg-red-700 transition"
        >
            Download JSON
        </button>
      </div>
</>
    )
}


export default DisplayJSON;