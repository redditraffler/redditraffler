import React, { useState } from "react";
import styled from "styled-components";
import useAsync from "react-use/lib/useAsync";
import { useFormContext } from "react-hook-form";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import Box from "react-bulma-components/lib/components/box";
import Loader from "react-bulma-components/lib/components/loader";
import Icon from "react-bulma-components/lib/components/icon";
import List from "react-bulma-components/lib/components/list";
import Columns from "react-bulma-components/lib/components/columns";
import Button from "react-bulma-components/lib/components/button";

import { getFromApi, Endpoint } from "@js/api";
import { GetUserSubmissionsAPIResponse } from "@js/types";
import { colors } from "@js/theme";
import { truncateStringAfterLength } from "@js/util";

dayjs.extend(relativeTime);

const BoxCenteredContent = styled(Box)`
  display: flex;
  justify-content: center;
`;

const ContentContainer = styled("div")`
  display: flex;
  justify-content: center;

  &:not(:last-child) {
    margin-bottom: 1rem;
  }
`;

const SubmissionListItem = styled(List.Item)`
  transition: 0.2s;

  &:not(.is-active):hover {
    background-color: ${colors.redditVeryLight};
    cursor: pointer;
  }

  &.is-active {
    background-color: ${colors.reddit};
    color: whitesmoke;

    /* Recolor links for contrast against is-active BG */
    & a {
      color: white;
      &:hover {
        color: ${colors.bulmaDarkGrayText};
      }
    }
  }
`;

const ShowMoreButtonContainer = styled("div")`
  display: flex;
  justify-content: center;
`;

const DEFAULT_NUM_SUBMISSIONS_TO_DISPLAY = 5;
const DEFAULT_SHOW_MORE_COUNT = 10;

const SubmissionPicker: React.FC = () => {
  const { register, setValue } = useFormContext();
  const { loading, error, value: userSubmissions } = useAsync(() =>
    getFromApi<GetUserSubmissionsAPIResponse>(
      Endpoint.getSubmissionsForCurrentUser
    )
  );
  const [selectedSubmissionId, setSelectedSubmissionId] = useState<
    string | undefined
  >(undefined);
  const [numSubmissionsToDisplay, setNumSubmissionsToDisplay] = useState<
    number
  >(DEFAULT_NUM_SUBMISSIONS_TO_DISPLAY);

  if (loading) {
    return (
      <BoxCenteredContent>
        <div>
          <ContentContainer>
            <Loader
              style={{
                width: "5rem",
                height: "5rem",
                border: `3px solid ${colors.reddit}`,
                borderTopColor: "transparent",
                borderRightColor: "transparent",
              }}
            />
          </ContentContainer>
          <ContentContainer>
            <p>Fetching your Reddit submissions...</p>
          </ContentContainer>
        </div>
      </BoxCenteredContent>
    );
  }

  if (error) {
    return (
      <BoxCenteredContent>
        <div>
          <ContentContainer>
            <Icon size="large">
              <span
                className="fas fa-times fa-4x"
                style={{ color: colors.errorText }}
              />
            </Icon>
          </ContentContainer>
          <ContentContainer>
            <p>
              An error occurred while trying to fetch your Reddit submissions.
              Please try again.
            </p>
          </ContentContainer>
        </div>
      </BoxCenteredContent>
    );
  }

  return (
    <React.Fragment>
      <input type="hidden" ref={register} name="submissionUrl" />
      <List>
        {userSubmissions && userSubmissions.length > 0
          ? userSubmissions.map(
              ({ subreddit, title, url, id, created_at_utc }, index) => {
                const createdAtDayjs = dayjs(created_at_utc * 1000);
                const shouldShowSubmission =
                  index + 1 <= numSubmissionsToDisplay;

                return shouldShowSubmission ? (
                  <SubmissionListItem
                    key={id}
                    onClick={() => {
                      setSelectedSubmissionId(id);
                      setValue("submissionUrl", url);
                    }}
                    className={id === selectedSubmissionId ? "is-active" : ""}
                  >
                    <Columns>
                      <Columns.Column>
                        <p className="has-text-weight-medium">
                          {truncateStringAfterLength(100, title)}
                        </p>
                      </Columns.Column>
                      <Columns.Column narrow>
                        <p className="has-text-right has-text-left-mobile">
                          in /r/{subreddit},{" "}
                          <span title={createdAtDayjs.toString()}>
                            {createdAtDayjs.from(dayjs())}
                          </span>
                          <a href={url} target="_blank" rel="noreferrer">
                            <Icon>
                              <span className="fas fa-external-link-alt fa-xs"></span>
                            </Icon>
                          </a>
                        </p>
                      </Columns.Column>
                    </Columns>
                  </SubmissionListItem>
                ) : null;
              }
            )
          : null}
      </List>
      {(userSubmissions?.length || 0) > numSubmissionsToDisplay ? (
        <ShowMoreButtonContainer>
          <Button
            outlined
            rounded
            size="small"
            onClick={() =>
              setNumSubmissionsToDisplay(
                numSubmissionsToDisplay + DEFAULT_SHOW_MORE_COUNT
              )
            }
          >
            Show More
          </Button>
        </ShowMoreButtonContainer>
      ) : null}
    </React.Fragment>
  );
};

export default SubmissionPicker;
