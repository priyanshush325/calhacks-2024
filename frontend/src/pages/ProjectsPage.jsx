import ProjectCard from "../components/ProjectCard";
const ProjectsPage = () => {
    return (
        <div className="grid grid-cols-3 gap-4 p-4">
            <ProjectCard
                title="Quick Click Cuisine"
                image="https://t3.ftcdn.net/jpg/02/52/38/80/360_F_252388016_KjPnB9vglSCuUJAumCDNbmMzGdzPAucK.jpg"
                link="https://google.com"
            />
            <ProjectCard
                title="LA Hacks Site"
                image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTa05Gk_HrLtqbecOYePU3TsX5GUma5MRJeLg&s"
                link="https://lahacks.com"
            />

            {/* Add more ProjectCards as needed */}
        </div>
    );
};

export default ProjectsPage;
