const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

function monthYear(value) {
  if (!value) return "";
  if (String(value).toLowerCase() === "present") return "present";
  const [y, m] = String(value).split("-");
  return m ? `${MONTHS[Number(m) - 1]} ${y}` : y;
}

module.exports = function (eleventyConfig) {
  // Content lives in /content (edited by Decap CMS); images in /assets; CMS in /admin.
  eleventyConfig.addWatchTarget("./content/");
  eleventyConfig.addPassthroughCopy({ "assets": "assets" });
  eleventyConfig.addPassthroughCopy({ "admin": "admin" });
  eleventyConfig.addPassthroughCopy({ "src/style.css": "style.css" });

  eleventyConfig.addFilter("monthYear", monthYear);
  eleventyConfig.addFilter("range", (start, end) => {
    const a = monthYear(start);
    const b = monthYear(end);
    return b && b !== a ? `${a} – ${b}` : a;
  });
  eleventyConfig.addFilter("isoDate", (d) => new Date(d).toISOString().slice(0, 10));

  return {
    dir: { input: "src", includes: "_includes", data: "_data", output: "_site" },
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
  };
};
