import React from "react";
import PropTypes from "prop-types";
import { useForm, FormProvider } from "react-hook-form";
import type { SubmitHandler } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers";
import Container from "react-bulma-components/lib/components/container";
import Columns from "react-bulma-components/lib/components/columns";
import Heading from "react-bulma-components/lib/components/heading";
import { Label } from "react-bulma-components/lib/components/form";
import styled from "styled-components";

import { colors } from "@js/theme";
import { newRaffleFormSchema } from "./schemas";
import type { NewRaffleFormSchema } from "./schemas";
import SubmissionPicker from "./SubmissionPicker";
import InputWithStaticButton from "./InputWithStaticButton";

const FormSectionContainer = styled(Container)`
  margin-bottom: 1rem;

  &:not(:first-child) {
    margin-top: 2rem;
  }
`;

interface NewRaffleProps {
  csrfToken: string;
}
const NewRaffle: React.FC<NewRaffleProps> = ({ csrfToken }) => {
  console.log({ csrfToken });

  const formMethods = useForm({
    resolver: yupResolver<NewRaffleFormSchema>(newRaffleFormSchema),
  });
  const { handleSubmit, register, watch } = formMethods;

  const isCombinedKarmaChecked = watch("usesCombinedKarma");

  const onSubmit: SubmitHandler<NewRaffleFormSchema> = async (d) => {
    console.log({ formdata: d });
  };

  return (
    <FormProvider {...formMethods}>
      <Container>
        <form
          onSubmit={handleSubmit(onSubmit, (err) => {
            console.log(formMethods.getValues());
            console.log(err);
          })}
        >
          <FormSectionContainer>
            <Columns>
              <Columns.Column>
                <Heading size={5}>
                  First, choose your Reddit submission.
                </Heading>
                <SubmissionPicker />
              </Columns.Column>
            </Columns>
          </FormSectionContainer>

          <FormSectionContainer>
            <Heading size={5}>
              Next, choose how many winners you&apos;d like for this raffle.
            </Heading>
            <Columns>
              <Columns.Column>
                <InputWithStaticButton
                  label="Number of Winners"
                  inputType="number"
                  name="winnerCount"
                  staticText="users"
                  defaultValue="1"
                  max="100"
                  min="1"
                />
              </Columns.Column>
            </Columns>
          </FormSectionContainer>

          <FormSectionContainer>
            <Heading size={5}>Set restrictions on user accounts.</Heading>
            <Columns>
              <Columns.Column>
                <InputWithStaticButton
                  label="Minimum Account Age"
                  inputType="number"
                  name="minAge"
                  staticText="days"
                  defaultValue="0"
                  min="0"
                />
              </Columns.Column>
            </Columns>
            <Columns>
              <Columns.Column>
                <Label>
                  <input
                    type="checkbox"
                    name="usesCombinedKarma"
                    ref={register}
                  />
                  <span style={{ marginLeft: "0.5rem", color: colors.reddit }}>
                    Select winners by combined karma
                  </span>
                </Label>
              </Columns.Column>
            </Columns>
            <Columns>
              {isCombinedKarmaChecked ? (
                <Columns.Column>
                  <InputWithStaticButton
                    label="Minimum Combined Karma"
                    inputType="number"
                    name="minCombined"
                    staticText="karma"
                    defaultValue="0"
                    min="0"
                  />
                </Columns.Column>
              ) : (
                <React.Fragment>
                  <Columns.Column size="one-third">
                    <InputWithStaticButton
                      label="Minimum Comment Karma"
                      inputType="number"
                      name="minComment"
                      staticText="karma"
                      defaultValue="0"
                      min="0"
                    />
                  </Columns.Column>
                  <Columns.Column size="one-third">
                    <InputWithStaticButton
                      label="Minimum Link Karma"
                      inputType="number"
                      name="minLink"
                      staticText="karma"
                      defaultValue="0"
                      min="0"
                    />
                  </Columns.Column>
                </React.Fragment>
              )}
            </Columns>
          </FormSectionContainer>
          <input type="submit" />
        </form>
      </Container>
    </FormProvider>
  );
};

NewRaffle.propTypes = {
  csrfToken: PropTypes.string.isRequired,
};

export default NewRaffle;
