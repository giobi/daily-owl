module.exports = function (eleventyConfig) {
  // Static assets
  eleventyConfig.addPassthroughCopy({ "src/css": "css" });
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });

  // Collections: published / drafts, by frontmatter `stato`
  eleventyConfig.addCollection("published", (c) =>
    c
      .getFilteredByGlob("src/posts/*.md")
      .filter((p) => p.data.stato === "published")
      .sort((a, b) => b.date - a.date)
  );
  eleventyConfig.addCollection("drafts", (c) =>
    c
      .getFilteredByGlob("src/posts/*.md")
      .filter((p) => p.data.stato === "draft")
      .sort((a, b) => b.date - a.date)
  );

  // Italian date filter
  const MESI = [
    "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
    "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre",
  ];
  eleventyConfig.addFilter("dataIt", (d) => {
    const dt = new Date(d);
    return `${dt.getUTCDate()} ${MESI[dt.getUTCMonth()]} ${dt.getUTCFullYear()}`;
  });
  eleventyConfig.addFilter("isoDate", (d) => new Date(d).toISOString());

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
  };
};
