module.exports = function (eleventyConfig) {
  // Tutti i link a fonti esterne aprono in nuova scheda (target=_blank + rel sicuro)
  eleventyConfig.amendLibrary("md", (md) => {
    const defaultRender =
      md.renderer.rules.link_open ||
      function (tokens, idx, options, env, self) {
        return self.renderToken(tokens, idx, options);
      };
    md.renderer.rules.link_open = function (tokens, idx, options, env, self) {
      const href = tokens[idx].attrGet("href") || "";
      if (/^https?:\/\//i.test(href)) {
        tokens[idx].attrSet("target", "_blank");
        tokens[idx].attrSet("rel", "noopener noreferrer");
      }
      return defaultRender(tokens, idx, options, env, self);
    };
  });

  // Static assets
  eleventyConfig.addPassthroughCopy({ "src/css": "css" });
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });
  eleventyConfig.addPassthroughCopy("src/favicon.svg");
  eleventyConfig.addPassthroughCopy("src/favicon-32.png");
  eleventyConfig.addPassthroughCopy("src/apple-touch-icon.png");
  eleventyConfig.addPassthroughCopy("src/favicon.ico");

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
