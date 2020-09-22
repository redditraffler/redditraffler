import React from "react";
import styled from "styled-components";
import useAsync from "react-use/lib/useAsync";
import Box from "react-bulma-components/lib/components/box";
import Loader from "react-bulma-components/lib/components/loader";
import Icon from "react-bulma-components/lib/components/icon";

import { getFromApi, Endpoint } from "@js/api";
import { GetUserSubmissionsAPIResponse } from "@js/types";
import { colors } from "@js/theme";

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

const SubmissionPicker: React.FC = () => {
  const { loading, error, value: userSubmissions } = useAsync(() =>
    getFromApi<GetUserSubmissionsAPIResponse>(
      Endpoint.getSubmissionsForCurrentUser
    )
  );

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

  return <Box>hello world</Box>;
};

export default SubmissionPicker;
