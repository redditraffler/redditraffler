export const escapeHtml = (str) =>
  str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");

export const truncateStringAfterLength = (truncateThreshold, string) => {
  const indexToCutOffString = truncateThreshold - 3;
  if (string.length < indexToCutOffString) {
    return string;
  }

  return `${string.substring(0, indexToCutOffString)}...`;
};
