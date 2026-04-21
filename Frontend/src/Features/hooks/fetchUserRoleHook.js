import { useEffect, useState } from "react";
import api from "../../api";
import { USER_ID } from "../../constants";
import getResponseMessages from "../../utils/extractResponseMessage";

export default function useFetchUserRole() {
  const [role, setRole] = useState("");
  const [response, setResponse] = useState(null);

  useEffect(() => {
    const fetchUserRole = async () => {
      const userId = localStorage.getItem(USER_ID);
      try {
        const res = await api.get(`api/users/${userId}/role/`);
        setRole(res.data.role);
      } catch (error) {
        setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
      }
    };
    fetchUserRole();
  }, []);

  return { role, response };
}
