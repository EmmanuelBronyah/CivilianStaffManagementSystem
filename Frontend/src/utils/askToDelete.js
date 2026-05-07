import Swal from "sweetalert2";
import style from "../styles/components/userscomponent.module.css";

const askToDelete = async (theme) => {
  const result = await Swal.fire({
    title: "Confirm Occurrence Deletion",
    text: "Are you sure you want to delete this occurrence?",
    showCancelButton: true,
    cancelButtonText: "No",
    confirmButtonText: "Yes",

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

export default askToDelete;
