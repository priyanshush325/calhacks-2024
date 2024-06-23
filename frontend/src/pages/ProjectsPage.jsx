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
            <ProjectCard
                title="Impact Personal Safety"
                image="https://static.wixstatic.com/media/c80174_fd3debb3de6243dea86adf6cb6743b1c~mv2.jpg/v1/crop/x_50,y_0,w_1100,h_718/fill/w_640,h_474,al_c,q_80,usm_0.66_1.00_0.01,enc_auto/Impact_06092022-131.jpg"
                link="https://impact.priyanshu.org"
            />

            {/* Add more ProjectCards as needed */}
        </div>
    );
};

export default ProjectsPage;
