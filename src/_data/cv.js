// Loads the CMS-editable JSON files from /content on every build.
const fs = require("fs");
const path = require("path");

const dir = path.join(__dirname, "..", "..", "content");
const read = (name) => JSON.parse(fs.readFileSync(path.join(dir, `${name}.json`), "utf8"));

module.exports = () => ({
  profile: read("profile"),
  education: read("education").items,
  experience: read("experience").items,
  skills: read("skills"),
  projects: read("projects"),
  chat: read("chat"),
});
