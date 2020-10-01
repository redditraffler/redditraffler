import * as yup from "yup";

export const newRaffleFormSchema = yup
  .object()
  .shape({
    submissionUrl: yup.string().required(),
    winnerCount: yup.number().min(1).required(),
    minAge: yup.number().min(0).required(),
    usesCombinedKarma: yup.bool().required(),
    minComment: yup.number().when("usesCombinedKarma", {
      is: false,
      then: yup.number().min(0).required(),
      otherwise: yup.number(),
    }),
    minLink: yup.number().when("usesCombinedKarma", {
      is: false,
      then: yup.number().min(0).required(),
      otherwise: yup.number(),
    }),
    minCombined: yup.number().when("usesCombinedKarma", {
      is: true,
      then: yup.number().min(0).required(),
      otherwise: yup.number(),
    }),
    ignoredUsers: yup.array().of(yup.string()).required(),
  })
  .required();

export type NewRaffleFormSchema = yup.InferType<typeof newRaffleFormSchema>;
