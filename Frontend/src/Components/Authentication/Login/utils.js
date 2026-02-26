export default function getResponseMessages(response) {
  const data = response.data;
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
  return firstMessage;
}
