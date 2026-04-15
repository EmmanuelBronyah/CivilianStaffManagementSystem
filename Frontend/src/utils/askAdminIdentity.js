import Swal from "sweetalert2";
import style from "../styles/components/userscomponent.module.css";
import api from "../api";
import getResponseMessages from "./extractResponseMessage";
import { USER_ID } from "../constants";

const showAskAdminIdentityModal = async (theme) => {
  const askForAdminPassword = async () => {
    const result = await Swal.fire({
      title: "Confirm Admin Password",
      input: "password",
      inputLabel: "Enter your password to continue",
      inputPlaceholder: "Enter password",
      inputAttributes: {
        autocapitalize: "off",
        autocorrect: "off",
      },
      showCancelButton: true,
      confirmButtonText: "Verify",

      customClass: {
        popup: `${style.customModal} ${!theme ? style.dark : ""}`,
        title: `${style.customTitle} ${!theme ? style.dark : ""}`,
        confirmButton: `${style.customConfirmBtn} ${!theme ? style.dark : ""}`,
        cancelButton: `${style.customCancelBtn} ${!theme ? style.dark : ""}`,
        input: `${style.customInput} ${!theme ? style.dark : ""}`,
      },
    });

    return result;
  };

  const result = await askForAdminPassword();
  return result;
};

const verifyAdminIdentity = async (
  verificationData,
  setLoading,
  setResponse,
) => {
  setLoading(true);
  try {
    const res = await api.post("api/users/verify/admin/", {
      data: verificationData,
    });
    return res.status;
  } catch (error) {
    if (error.response.status === 401) {
      setLoading(false);
      return error.response.status;
    } else {
      setLoading(false);
      setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });
      return;
    }
  }
};

export default async function verifyAdminProcess(
  theme,
  setLoading,
  setResponse,
) {
  const result = await showAskAdminIdentityModal(theme);

  if (!result.isConfirmed) {
    return;
  }

  const userID = localStorage.getItem(USER_ID);
  const verificationData = {
    id: userID,
    adminPassword: result.value,
  };

  const status = await verifyAdminIdentity(
    verificationData,
    setLoading,
    setResponse,
  );

  return status;
}

export async function showErrorModal(theme) {
  await Swal.fire({
    title: "Error",
    text: "Invalid Credentials",
    icon: "error",
    confirmButtonText: "OK",

    customClass: {
      popup: `${style.customModal} ${!theme ? style.dark : ""}`,
      title: `${style.customTitle} ${!theme ? style.dark : ""}`,
      confirmButton: `${style.customConfirmBtn} ${!theme ? style.dark : ""}`,
    },
  });
}
