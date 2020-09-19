import React from "react";
import PropTypes from "prop-types";
import * as yup from "yup";
import { useForm, FormProvider, useFormContext } from "react-hook-form";
import type { SubmitHandler } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers";
import Container from "react-bulma-components/lib/components/container";
import Columns from "react-bulma-components/lib/components/columns";
import Heading from "react-bulma-components/lib/components/heading";

const newRaffleFormSchema = yup
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

type NewRaffleFormSchema = yup.InferType<typeof newRaffleFormSchema>;

interface NewRaffleProps {
  csrfToken: string;
}
const NewRaffle: React.FC<NewRaffleProps> = ({ csrfToken }) => {
  console.log({ csrfToken });

  const formMethods = useForm({
    resolver: yupResolver<NewRaffleFormSchema>(newRaffleFormSchema),
  });

  const onSubmit = async () => {
    console.log("hello world");
  };

  return (
    <FormProvider {...formMethods}>
      <Container>
        <form onSubmit={formMethods.handleSubmit(onSubmit)}>
          <Columns>
            <Columns.Column>
              <Heading size={5}>First, choose your Reddit submission.</Heading>
            </Columns.Column>
          </Columns>
        </form>
      </Container>
    </FormProvider>
  );
};

NewRaffle.propTypes = {
  csrfToken: PropTypes.string.isRequired,
};

export default NewRaffle;
