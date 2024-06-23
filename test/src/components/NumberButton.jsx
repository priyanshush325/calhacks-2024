import { stringToColor } from "../utils/helpers";
const NumberButton = ({ value, onClick, additionalClasses = "" }) => {
    return (
        <button
            className={`text-white font-medium py-2 px-4 rounded ${stringToColor(value)} ${additionalClasses}`}
            onClick={onClick}
        >
            {value}
        </button>
    );
};

export default NumberButton;
