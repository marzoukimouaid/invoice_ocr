



const Loading = () => {
    return (<div className="flex flex-col items-center justify-center py-10 px-4 text-center animate-pulse">
            <svg className="w-12 h-12 text-red-600 mb-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z">
                </path>
            </svg>
            <p className="text-lg font-medium text-gray-700">Extracting data…</p>
            <p className="text-sm text-gray-500 mt-1">This might take a few seconds depending on file size.</p>
        </div>
    );
}


export default Loading;