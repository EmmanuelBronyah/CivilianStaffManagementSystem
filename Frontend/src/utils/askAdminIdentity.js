import Swal from "sweetalert2";
import style from "../styles/components/userscomponent.module.css";

export default async function showAskAdminIdentityModal(theme) {
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
