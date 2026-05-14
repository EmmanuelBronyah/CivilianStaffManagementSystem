export default function getResponseMessages(response) {
  const data = response.data;

  const messages = [];

  if (data) {
    const keyValuePairs = Object.entries(data);
    console.log(keyValuePairs);

    if (keyValuePairs) {
      for (const [key, value] of Object.entries(data)) {
        if (key === "detail") {
          messages.push(`${value}`);
        } else {
          let capitalizedKey = key.charAt(0).toUpperCase() + key.slice(1);
          capitalizedKey = capitalizedKey.replace("_", " ");

          if (capitalizedKey === "Non_field_errors") {
            messages.push(`${value}`);
          } else {
            messages.push(`${capitalizedKey}: ${value}`);
          }
        }
      }
    } else {
      for (const obj in data) {
        messages.push(obj);
      }
    }
  }

  let firstMessage = messages[0];
  firstMessage = firstMessage.replaceAll("_", " ");
  return firstMessage;
}
