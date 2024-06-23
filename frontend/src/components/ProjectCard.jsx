import { useNavigate } from "react-router-dom";

const ProjectCard = ({ title, image, link = "https://google.com" }) => {
    const navigate = useNavigate();

    const handleClick = () => {
        if (link.startsWith("http")) {
            window.open(link, "_blank", "noopener,noreferrer");
        } else {
            navigate(link);
        }
    };

    return (
        <div className="relative cursor-pointer" onClick={handleClick}>
            <img src={image} alt={title} className="w-full h-full object-cover" />
            <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                <span className="text-white text-xl font-bold">{title}</span>
            </div>
        </div>
    );
};

export default ProjectCard;
