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
    return false;
  }
}

function getResponseMessages(response) {
  const data = response.data;
  console.log("Response Data -> ", data);

  const messages = [];

  if (data) {
    const keyValuePairs = Object.entries(data);
    console.log("Key Value Pairs", keyValuePairs);

    if (keyValuePairs) {
      for (const [key, value] of Object.entries(data)) {
        if (key === "detail") {
          messages.push(`${value}`);
        } else {
          const capitalizedKey = key.charAt(0).toUpperCase() + key.slice(1);
          messages.push(`${capitalizedKey}: ${value}`);
        }
      }
    } else {
      for (const obj in data) {
        messages.push(obj);
      }
    }
  }
  const firstMessage = messages[0];
  console.log("First Message -> ", firstMessage);
  return firstMessage;
}

export { checkInternetConnection, getResponseMessages };
