import { FaSearch, FaUser } from "react-icons/fa";
import "../index.css";
import MenuBar from "./MenuBar";

/** Adding shadow to the top of the menu bar */

const DashboardPage = () => {
    return (
        <div className="p-6 bg-gray-50 min-h-screen">
            <div className="flex justify-between items-center mb-4">
                <h1 className="text-3xl font-bold">DEMO</h1>
                <div className="w-24 h-24 bg-gray-300 rounded-full"></div>
            </div>
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-normal">My Family</h2>
                <div className="relative flex items-center">
                    <input
                        type="text"
                        placeholder="Search"
                        className="p-2 pl-10 border-2 border-teal-500 rounded-full bg-white w-40 md:w-64"
                    />
                    <FaSearch className="absolute left-3 w-5 h-5 text-black" />
                </div>
            </div>
            <div className="mb-8"></div>
            <div className="flex justify-between items-center mb-4">
                <div className="w-20 h-20 bg-gray-300 rounded-full border border-teal-500 mr-6"></div>
                <div className="p-3 bg-white border border-teal-500 rounded-lg flex-1 max-w-xs h-28">
                    <h2 className="text-xl font-semibold">Fred Sharma, 14</h2>
                    <p className="text-sm text-gray-600 flex items-center gap-2">
                        <FaUser className="inline-block w-4 h-4 ml-2" />
                        Me
                    </p>
                    <p className="text-sm text-gray-600 flex items-center gap-2">
                        <FaUser className="inline-block w-4 h-4 ml-2" />
                        Diabetes, Hypertension
                    </p>

                </div>
            </div>
            <div className="grid gap-6 mb-8 md:grid-cols-2 lg:grid-cols-3">
                {/* User Stats Section */}
                <div className="p-4 bg-white rounded-lg shadow-md">
                    <h2 className="text-xl font-semibold mb-2">User Stats</h2>
                    {/* Dummy user stats for now */}
                    <p>Total Activities: 50</p>
                    <p>Completed Tasks: 30</p>
                    <p>Pending Tasks: 20</p>
                </div>
                {/* Recent Activities Section */}
                <div className="p-4 bg-white rounded-lg shadow-md">
                    <h2 className="text-xl font-semibold mb-2">Recent Activities</h2>
                    {/* Dummy recent activities for now */}
                    <ul>
                        <li>Completed Task 1</li>
                        <li>Completed Task 2</li>
                        <li>Started Task 3</li>
                    </ul>
                </div>
            </div>
            <div className="fixed bottom-0 left-0 w-full p-4 bg-white shadow-lg">
                <MenuBar />
            </div>
        </div>
    );
};

export default DashboardPage;
