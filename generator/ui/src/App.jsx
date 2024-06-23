import { useState } from "react";
import TextareaAutosize from "react-textarea-autosize";
import "./App.css";

const baseUrl = import.meta.env.VITE_PROJECT_URL;
const serverUrl = import.meta.env.VITE_SERVER_URL;

async function sendMessage(message) {
	response = await fetch(serverUrl + "/message", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ message }),
	});
}

async function sendProject(project) {
	response = await fetch(serverUrl + "/project", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: {
			projectName: project.name,
			projectSourceDir: project.path,
		},
	});
}

function App() {
	const [project, setProject] = useState({
		name: "It literally doesn't matter",
		path: "",
	});
	const [projectSet, setProjectSet] = useState(false);

	const [url, setUrl] = useState(baseUrl);
	const [urlBar, setUrlBar] = useState(baseUrl);
	const [message, setMessage] = useState("");

	return (
		<>
			<div className="page">
				<div className="content">
					<div>
						<form
							className="url-bar-container"
							onSubmit={(e) => {
								e.preventDefault();
								setUrl(urlBar);
							}}
						>
							<input
								className="url-bar"
								type="text"
								value={urlBar}
								onChange={(e) => setUrlBar(e.target.value)}
							/>
						</form>
					</div>
					<div className="iframe-container">
						{projectSet && (
							<iframe
								src={url}
								title="iframe"
								// width="100%"
								id="iframe"
							></iframe>
						)}
						{!projectSet && (
							<div className="chat-settings">
								<h1>Select a Project</h1>
								{/* <input
									type="text"
									placeholder="Project name"
									onChange={(e) =>
										setProject({ ...project, name: e.target.value })
									}
								/> */}
								<input
									type="text"
									placeholder="Absolute project path"
									onChange={(e) =>
										setProject({ ...project, path: e.target.value })
									}
								/>
								<button>Submit</button>
							</div>
						)}
					</div>
				</div>
				<div className="chat">
					<div
						style={{
							flex: 1,
						}}
					></div>

					<TextareaAutosize
						className="message-box"
						type="text"
						placeholder="Enter a prompt..."
						value={message}
						onChange={(e) => setMessage(e.target.value)}
						onKeyDown={(e) => {
							if (e.key === "Enter") {
								e.preventDefault();

								console.log("Enter pressed");
								if (message === "") return;

								sendMessage(message);
								setMessage("");
							}
						}}
					/>
				</div>
			</div>
		</>
	);
}

export default App;
