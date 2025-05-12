import { useState } from "react";
import api from "../../../api";
import { extractErrorMessages, checkInternetConnection } from "../../../utils";

function ResetPassword({ route }) {
  const [email, setEmail] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const hasInternetConnection = await checkInternetConnection();

    if (!hasInternetConnection) {
      console.log(
        "Network issue detected. Please ensure you are connected to the internet and try again."
      );
      return;
    }

    try {
      const res = await api.post(route, { email: email });
      if (res.status === 200) {
        console.log(res.data.detail);
      }
    } catch (error) {
      let errorData = error.response.data;
      const messages = extractErrorMessages(errorData);
      for (const message of messages) {
        console.log("Error message:", message);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
        />
      </div>
      <button type="submit">Submit</button>
    </form>
  );
}

export default ResetPassword;
