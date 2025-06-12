import { useState } from "react";
import api from "../../../api";
import { checkInternetConnection } from "../../../utils";

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
        console.log("Response: ", res.data.detail);
      }
    } catch (error) {
      if (error.response.status === 429) {
        console.log(
          "Too many requests were made. Please try again after sometime."
        );
      }
      if (error.response) {
        console.log("Error: ", error.response.data);
      } else {
        console.log("Unexpected Error: ", error);
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
