import { useState } from "react";
import TextareaAutosize from "react-textarea-autosize";
import "./App.css";

const baseUrl = import.meta.env.VITE_PROJECT_URL;
const serverUrl = import.meta.env.VITE_SERVER_URL;

async function sendMessage(message) {
	let response = await fetch(serverUrl + "/prompt", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			prompt: message,
		}),
	});

	return response.status === 200;
}

async function confirmActions(confirm) {
	let response = await fetch(serverUrl + "/confirm", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			confirm: confirm,
		}),
	});

	const data = await response.json();
	console.log(data);

	return response.status === 200;
}

async function sendProject(project) {
	console.log(project);
	let response = await fetch(serverUrl + "/info", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			// projectName: project.name,
			projectSourceDir: project.path,
		}),
	});

	console.log(response);

	return response.status === 200;
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
	const [awaitingConfirmation, setAwaitingConfirmation] = useState(false);

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
								<button
									onClick={async () => {
										let successs = await sendProject(project);
										if (successs) {
											setProjectSet(true);
										}
									}}
								>
									Submit
								</button>
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
						placeholder={
							awaitingConfirmation
								? "Enter to confirm, anything else to cancel..."
								: "Enter a prompt..."
						}
						value={message}
						onChange={(e) => setMessage(e.target.value)}
						onKeyDown={(e) => {
							if (e.key === "Enter") {
								e.preventDefault();

								console.log("Enter pressed");

								if (awaitingConfirmation) {
									if (message === "") {
										confirmActions(true);
										setMessage("");
										setAwaitingConfirmation(false);
									} else {
										confirmActions(false);
										setMessage("");
										setAwaitingConfirmation(false);
									}
								} else {
									if (message === "") return;

									sendMessage(message);
									setMessage("");
								}
							}
						}}
					/>
				</div>
			</div>
		</>
	);
}

export default App;
