import React, {useState} from "react";


const LlmForm = () => {const [isFetching, setIsFetching] = useState(false);
  const [fetchedData, setFetchedData] = useState();
  const [errors, setErrors] = useState('');
  const [img, setImage] = useState();
    function handleImageChange(e) {
    setImage(e.target.files[0])
    setErrors('');
  }

    return (
        <div className="bg-white shadow-md rounded-xl p-8 w-full max-w-2xl mx-auto mt-8">
            <form>
                <h2 className="text-2xl font-bold text-red-600 ">LLM Base Extraction</h2>
                <p className="mb-6">Higher Latency, Higher Accuracy</p>
                {/* File Input */}
                <div className='pb-5'>
                    <label
                        htmlFor="fileInput"
                        className="block text-sm font-medium text-gray-700 mb-1 pb-5"
                    >
                        Upload Image or PDF
                    </label>
                    <input
                        id="fileInput"
                        type="file"
                        accept="image/*,.pdf"

                        className="block w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 text-sm file:bg-red-600
          file:text-white file:border-none file:rounded file:px-4 file:py-2 hover:file:bg-red-700 transition"
                    />
                </div>

                {/* Custom Instructions */}


                {/* Submit Button */}
                <div className="text-right">
                    <button
                        type="submit"
                        className="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-6 rounded transition duration-200"
                    >
                        Extract
                    </button>
                </div>
            </form>
        </div>
    )
}


export default LlmForm;