import React from "react";
import { render, waitFor } from "@testing-library/react";

import Emoji from "./Emoji";

const testEmoji = "😈";

test("renders the emoji with the correct props", async () => {
  const testId = "emojiComponent";
  const { getByTestId } = render(
    <Emoji symbol={testEmoji} data-testid={testId} />
  );

  const component = await waitFor(() => getByTestId(testId));

  expect(component).toHaveTextContent(testEmoji);
  expect(component).toHaveAttribute("aria-label", "");
  expect(component).toHaveAttribute("aria-hidden", "true");
});
