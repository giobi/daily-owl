module.exports = {
  layout: "post.njk",
  tags: ["posts"],
  eleventyComputed: {
    // Published -> /{slug}/  ·  Draft -> /drafts/{slug}/
    permalink: (data) => {
      const slug = data.page.fileSlug;
      return data.stato === "draft"
        ? `drafts/${slug}/index.html`
        : `${slug}/index.html`;
    },
  },
};
