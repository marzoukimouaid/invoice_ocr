

const FetchingError = ({error}) => {
    return (
        <div
            className="bg-red-100 border border-red-300 text-red-800 px-6 py-4 rounded-xl max-w-xl mx-auto flex items-start space-x-3">

            <svg className="w-6 h-6 mt-1 flex-shrink-0 text-red-600" fill="none" viewBox="0 0 24 24"
                 stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                      d="M12 9v2m0 4h.01M12 5.5a6.5 6.5 0 110 13 6.5 6.5 0 010-13z"/>
            </svg>


            <div>
                <p className="font-semibold text-base">Something went wrong</p>
                <p className="text-sm mt-1">{error}</p>

            </div>
        </div>

    )


}


export default FetchingError;