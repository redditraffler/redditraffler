import React, { useState } from "react";
import { useFormContext } from "react-hook-form";
import {
  Field,
  Control,
  Input,
  Label,
  Help,
} from "react-bulma-components/lib/components/form";
import Button from "react-bulma-components/lib/components/button";
import Columns from "react-bulma-components/lib/components/columns";
import Tag from "react-bulma-components/lib/components/tag";

import { colors } from "@js/theme";

const DEFAULT_IGNORED_USERS_LIST = ["AutoModerator"];

const IgnoredUsersManager: React.FC = () => {
  const { control } = useFormContext();
  const [currentTextInput, setCurrentTextInput] = useState<string>("");
  const [isCurrentUserValid, setIsCurrentUserValid] = useState<boolean>(false);
  const [ignoredUsersList, setIgnoredUsersList] = useState<Array<string>>(
    DEFAULT_IGNORED_USERS_LIST
  );

  const shouldShowValidationError =
    currentTextInput !== "" && !isCurrentUserValid;

  /**
   * Returns if a username is a valid Reddit username and checks whether
   * that user is already ignored.
   * @param user The username to test
   */
  const isValidUser = (user: string) => {
    const USERNAME_REGEX = /^[\w-]+$/;
    const ignoredUsersSetLowercase = new Set(
      ignoredUsersList.map((u) => u.toLowerCase())
    );
    return (
      user.length >= 3 &&
      user.length <= 20 &&
      USERNAME_REGEX.test(user) &&
      !ignoredUsersSetLowercase.has(user)
    );
  };

  /**
   * Adds an ignored user by setting the appropriate backend state values.
   * @param user The username to add to the list backend
   */
  const addIgnoredUser = (user: string) => {
    setIsCurrentUserValid(true);
    setIgnoredUsersList([...ignoredUsersList, user]);
    setCurrentTextInput(""); // Clear input on successful add
  };

  /**
   * Removes the given user from the ignoredUsersList
   * @param user The user to remove
   */
  const removeIgnoredUser = (user: string) => {
    setIgnoredUsersList(
      ignoredUsersList.filter((u) => u.toLowerCase() !== user.toLowerCase())
    );
  };

  return (
    <React.Fragment>
      <Label style={{ color: colors.reddit }}>Ignored Users</Label>
      <Help style={{ paddingBottom: "1rem" }}>
        Use this field to add usernames, such as the submission&apos;s author or
        bots like <code>AutoModerator</code>, that you want to exclude from this
        raffle.
        <br />
        Usernames are case-insensitive.
      </Help>
      <Columns>
        <Columns.Column narrow>
          <Field kind="addons">
            <Control>
              <span className="button is-static">/u/</span>
            </Control>
            <Control>
              <Input
                type="text"
                color={shouldShowValidationError ? "danger" : null}
                value={currentTextInput}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                  setIsCurrentUserValid(isValidUser(e.target.value));
                  setCurrentTextInput(e.target.value);
                }}
                onKeyPress={(e: React.KeyboardEvent<HTMLInputElement>) => {
                  if (e.key !== "Enter") {
                    return;
                  }

                  e.preventDefault(); // Stop the whole form from submitting
                  if (isCurrentUserValid) {
                    addIgnoredUser(currentTextInput);
                  }
                }}
              />
            </Control>
            <Control>
              <Button
                disabled={!isCurrentUserValid}
                style={{ backgroundColor: colors.reddit, color: "whitesmoke" }}
                onClick={() => addIgnoredUser(currentTextInput)}
              >
                Ignore
              </Button>
            </Control>
          </Field>
        </Columns.Column>
        <Columns.Column>
          {ignoredUsersList.map((user) => (
            <Tag
              key={user}
              rounded
              style={{ backgroundColor: colors.reddit, color: "whitesmoke" }}
              size="medium"
            >
              {user}
              <Button remove onClick={() => removeIgnoredUser(user)} />
            </Tag>
          ))}
        </Columns.Column>
      </Columns>
    </React.Fragment>
  );
};

export default IgnoredUsersManager;
