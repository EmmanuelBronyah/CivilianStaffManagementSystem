import { displayLabels } from "../Components/AdvancedSearch/constants";

export const validateFormData = (formData) => {
  if (Object.keys(formData).length < 1) {
    return;
  }

  for (const [record, recordValue] of Object.entries(formData)) {
    if (Object.keys(recordValue).length < 1) {
      continue;
    }

    for (const [label, labelValue] of Object.entries(recordValue)) {
      if (labelValue === null || labelValue === "") {
        return `${record} - ${displayLabels[record][label]} cannot be empty.`;
      }

      if (typeof labelValue === "object") {
        if (Object.keys(labelValue).length < 1) {
          return `${record} - ${displayLabels[record][label]} cannot be empty.`;
        }

        for (const [key, value] of Object.entries(labelValue)) {
          if (key === "between") {
            const { from, to } = value;

            if (!("from" in value) || from === "" || from === null) {
              return `${record} - ${displayLabels[record][label]} 'from' field cannot be empty.`;
            }
            if (!("to" in value) || to === "" || to === null) {
              return `${record} - ${displayLabels[record][label]} 'to' field cannot be empty.`;
            }

            if (label.toLowerCase().includes("date")) {
              const fromDate = new Date(from);
              const toDate = new Date(to);

              if (fromDate > toDate) {
                return `${record} - ${displayLabels[record][label]} 'from' date field cannot be greater than 'to' date field.`;
              }
            } else {
              if (Number(from) > Number(to)) {
                return `${record} - ${displayLabels[record][label]} 'from' field cannot be greater than 'to' field.`;
              }
            }
          }
        }
      }
    }

    return true;
  }
};
