import React, { useState } from "react";
import useAsync from "react-use/lib/useAsync";
import styled from "styled-components";

import Container from "react-bulma-components/lib/components/container";
import Columns from "react-bulma-components/lib/components/columns";
import Loader from "react-bulma-components/lib/components/loader";
import Heading from "react-bulma-components/lib/components/heading";
import Button from "react-bulma-components/lib/components/button";

import { Endpoint, getFromApi } from "@js/api";
import { colors } from "@js/theme";

import RaffleListItem from "./RaffleListItem";

const DEFAULT_NUM_RAFFLES_TO_DISPLAY = 10;
const DEFAULT_SHOW_MORE_COUNT = 10;

const ShowMoreButtonContainer = styled("div")`
  display: flex;
  justify-content: center;
  margin-top: 2rem;
`;

/**
 * The main container for the RecentRaffles component.
 */
const RecentRaffles = () => {
  const { loading, error, value: raffles } = useAsync(() =>
    getFromApi(Endpoint.getRecentRaffles)
  );
  const [numRafflesToDisplay, setNumRafflesToDisplay] = useState(
    DEFAULT_NUM_RAFFLES_TO_DISPLAY
  );

  if (loading || error) {
    return (
      <Container>
        <Columns centered>
          <Columns.Column
            size="one-quarter"
            style={{ display: "flex", justifyContent: "center" }}
          >
            {loading ? (
              <Loader
                style={{
                  width: "2rem",
                  height: "2rem",
                  border: `2px solid ${colors.reddit}`,
                  borderTopColor: "transparent",
                  borderRightColor: "transparent",
                }}
              />
            ) : (
              <p>Couldn&apos;t fetch recent raffles :(</p>
            )}
          </Columns.Column>
        </Columns>
      </Container>
    );
  }

  return (
    <Container>
      <Columns centered>
        <Columns.Column size={8}>
          <Heading
            style={{
              display: "flex",
              justifyContent: "center",
              color: colors.reddit,
            }}
          >
            Recent Raffles
          </Heading>
          {raffles.map(
            (
              {
                created_at,
                submission_title,
                submission_id,
                subreddit,
                url_path,
              },
              index
            ) => {
              const shouldShowRaffle = index + 1 <= numRafflesToDisplay;
              return shouldShowRaffle ? (
                <RaffleListItem
                  key={index}
                  createdAt={created_at}
                  submissionTitle={submission_title}
                  submissionId={submission_id}
                  subreddit={subreddit}
                  urlPath={url_path}
                />
              ) : null;
            }
          )}
          {raffles.length > numRafflesToDisplay ? (
            <ShowMoreButtonContainer>
              <Button
                outlined
                rounded
                size="small"
                onClick={() =>
                  setNumRafflesToDisplay(
                    numRafflesToDisplay + DEFAULT_SHOW_MORE_COUNT
                  )
                }
              >
                Show More
              </Button>
            </ShowMoreButtonContainer>
          ) : null}
        </Columns.Column>
      </Columns>
    </Container>
  );
};

export default RecentRaffles;
