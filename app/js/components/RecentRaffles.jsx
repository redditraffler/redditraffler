import React from "react";
import useAsync from "react-use/lib/useAsync";
import styled from "styled-components";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";

import Container from "react-bulma-components/lib/components/container";
import Columns from "react-bulma-components/lib/components/columns";
import Loader from "react-bulma-components/lib/components/loader";
import Box from "react-bulma-components/lib/components/box";
import Tile from "react-bulma-components/lib/components/tile";
import Heading from "react-bulma-components/lib/components/heading";
import Element from "react-bulma-components/lib/components/element";

import { getRecentRaffles } from "@js/api";
import { colors } from "@js/theme";
import { getRandomElement, truncateStringAfterLength } from "@js/util";
import Emoji from "./Emoji";

dayjs.extend(relativeTime);

const RaffleListItemEmojis = ["🍀", "🎁", "🏆", "🌟", "🏅", "🎉", "🎊"];

const VCenteredTile = styled(Tile)`
  display: flex;
  align-items: center;
`;

const RaffleListItemContainer = styled(Box)`
  && {
    padding-top: 0rem;
    padding-bottom: 0rem;
  }

  transition: all 0.2s ease-in-out;

  a {
    color: ${colors.bulmaDarkGrayText}; /* Need to override link styling in app.scss */
  }

  &:hover {
    transform: scale(1.05);
  }
`;

const RecentRaffles = () => {
  const { loading, error, value: raffles } = useAsync(getRecentRaffles);

  console.log({ raffles });

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
            title
            style={{
              display: "flex",
              justifyContent: "center",
              color: colors.reddit,
            }}
          >
            Recent Raffles
          </Heading>
          {raffles.map(
            ({ created_at, submission_title, submission_id, subreddit }) => {
              const createdAtDayjs = dayjs(created_at * 1000);

              return (
                <RaffleListItemContainer key={submission_id}>
                  <a href={`/raffles/${submission_id}`}>
                    <Tile kind="ancestor">
                      <Tile kind="parent" size={1}>
                        <VCenteredTile kind="child">
                          <Emoji
                            symbol={getRandomElement(RaffleListItemEmojis)}
                            style={{ display: "block", fontSize: "3rem" }}
                          />
                        </VCenteredTile>
                      </Tile>
                      <Tile kind="parent">
                        <VCenteredTile kind="child">
                          <div>
                            <Element
                              renderAs="p"
                              className="is-size-6 has-text-weight-medium"
                              style={{ marginBottom: "0.5rem" }}
                              title={submission_title}
                            >
                              {truncateStringAfterLength(100, submission_title)}
                            </Element>
                            <Heading heading renderAs="p">
                              /r/{subreddit}
                            </Heading>
                          </div>
                        </VCenteredTile>
                      </Tile>
                      <Tile kind="parent" size={2}>
                        <VCenteredTile
                          kind="child"
                          style={{ justifyContent: "flex-end" }}
                        >
                          <Element
                            renderAs="p"
                            className="is-size-7"
                            title={createdAtDayjs.toString()}
                          >
                            {createdAtDayjs.from(dayjs())}
                          </Element>
                        </VCenteredTile>
                      </Tile>
                    </Tile>
                  </a>
                </RaffleListItemContainer>
              );
            }
          )}
        </Columns.Column>
      </Columns>
    </Container>
  );
};

export default RecentRaffles;
