import { FaUser } from "react-icons/fa";
import "../App.css";

const HomePage = () => {
    return (
        <div className="flex items-center justify-center min-h-screen">
            <h2 className="text-lg">My family</h2>
            <h1>Home</h1>
            <div className="flex mt-4">
                <FaUser className="h-16 w-16 border-2 border-teal-500" />
                <div className="ml-4 p-2 border-2 border-teal-500 space-x-2">
                    <p className="text-sm">Info box content</p>
                    flex flex-col
                </div>
            </div>
        </div>
    );
};

export default HomePage;
