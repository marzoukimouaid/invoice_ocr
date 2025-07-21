


const SuccessNotif = ({message}) => {
    return (
        <div
            className="bg-green-100 border border-green-300 text-green-800 px-6 py-4 rounded-xl max-w-xl mx-auto flex items-start space-x-3">

            <svg className="w-6 h-6 mt-1 flex-shrink-0 text-green-600" fill="none" viewBox="0 0 24 24"
                 stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                      d="M5 13l4 4L19 7"/>
            </svg>

            <div>
                <p className="font-semibold text-base">Success</p>
                <p className="text-sm mt-1">{message}</p>
            </div>
        </div>
    )
}



export default SuccessNotif;