import { FaBars, FaBook, FaSearch, FaUser, FaUsers } from "react-icons/fa";
import { Link } from "react-router-dom";

/** Adjusting the height of the menu bar to make it shorter, adding more spacing between the icons, and ensuring icons are vertically centered */

const MenuBar = () => {

    return (
        <div className="mt-4 h-12">

            <div className="flex justify-evenly items-center space-x-8">
                <Link to="/menu" className="text-blue-500 hover:underline">
                    <FaBars className="text-black text-2xl" />
                </Link>
                <Link to="/group" className="text-blue-500 hover:underline">
                    <FaUsers className="text-black text-2xl" />
                </Link>
                <Link to="/book" className="text-blue-500 hover:underline">
                    <FaBook className="text-black text-2xl" />
                </Link>
                <Link to="/profile" className="text-blue-500 hover:underline">
                    <FaUser className="text-black text-2xl" />
                </Link>
            </div>
        </div>
    );
};

export default MenuBar;
