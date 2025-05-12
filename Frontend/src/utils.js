function extractErrorMessages(data) {
  const messages = [];

  function recurse(obj) {
    if (Array.isArray(obj)) {
      obj.forEach((item) => recurse(item));
    } else if (typeof obj === "object" && obj !== null) {
      Object.values(obj).forEach((value) => recurse(value));
    } else if (typeof obj === "string") {
      messages.push(obj);
    }
  }

  recurse(data);
  return messages;
}

async function checkInternetConnection() {
  try {
    const timeoutId = 3000;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), timeoutId);

    const res = await fetch("https://jsonplaceholder.typicode.com/posts/1", {
      method: "GET",
      signal: controller.signal,
    });

    clearTimeout(timeout);
    return res.ok;
  } catch (error) {
    console.log("NO INTERNET");
    return false;
  }
}

export { extractErrorMessages, checkInternetConnection };
