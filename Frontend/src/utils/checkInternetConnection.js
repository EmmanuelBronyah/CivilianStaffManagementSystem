export default async function checkInternetConnection() {
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
