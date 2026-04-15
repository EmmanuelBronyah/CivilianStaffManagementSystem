import Swal from "sweetalert2";
import style from "../styles/components/userscomponent.module.css";
import verifyAdminProcess from "./askAdminIdentity";
import { showErrorModal } from "./askAdminIdentity";
import getResponseMessages from "./extractResponseMessage";
import api from "../api";
import { USER_ID } from "../constants";

async function askUserAccessModal(theme, title, question) {
  const result = await Swal.fire({
    title: title,
    text: question,
    showCancelButton: true,
    cancelButtonText: "No",
    confirmButtonText: "Yes",

    customClass: {
      popup: `${style.customModal} ${!theme ? style.dark : ""}`,
      title: `${style.customTitle} ${!theme ? style.dark : ""}`,
      confirmButton: `${style.customConfirmBtn} ${!theme ? style.dark : ""}`,
      cancelButton: `${style.customCancelBtn} ${!theme ? style.dark : ""}`,
    },
  });

  return result;
}

export default async function manageUserAccessProcess(
  theme,
  action,
  userId,
  setLoading,
  setResponse,
  title,
  question,
  email,
) {
  const result = await askUserAccessModal(theme, title, question);

  if (!result.isConfirmed) return;

  const status = await verifyAdminProcess(theme, setLoading, setResponse);

  if (status === 401) {
    await showErrorModal(theme);
    return;
  } else if (status === 200) {
    let res;
    let message;

    const storedId = Number(localStorage.getItem(USER_ID));
    const sameUser = storedId === userId;

    switch (action) {
      case "deactivate":
        res = await api.delete(`api/users/deactivate/${userId}/`);
        message = "User Account deactivated";
        break;
      case "restore":
        res = await api.patch(`api/users/restore/${userId}/`);
        message = "User Account restored";
        break;
      case "passwordReset":
        res = await api.post("api/auth/password/reset/", { email: email });
        message = `Password Rest link sent to user's email - ${email}`;
        break;
      case "delete":
        if (sameUser) {
          setLoading(false);
          setResponse({
            message: "This action cannot be done",
            type: "error",
            id: Date.now(),
          });
          return;
        }
        res = await api.delete(`api/users/delete/${userId}/`);
        message = "User Account deleted";
        break;
      default:
        break;
    }

    try {
      if (res.status === 200) {
        setLoading(false);
        setResponse({
          message: message,
          id: Date.now(),
        });
        return "DEACTIVATED | RESTORED";
      } else if (action === "delete" && res.status === 204) {
        setLoading(false);
        setResponse({
          message: message,
          id: Date.now(),
        });
        return "DELETED";
      }
    } catch (error) {
      setLoading(false);
      setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });
      return;
    }
  }
}
