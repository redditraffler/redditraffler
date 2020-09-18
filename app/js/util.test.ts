import * as util from "./util";

describe("escapeHtml", () => {
  it("escapes all the expected characters", () => {
    expect(util.escapeHtml("&<>\"'")).toEqual("&amp;&lt;&gt;&quot;&#039;");
  });
});

describe("truncateStringAfterLength", () => {
  describe("when the string is below the threshold", () => {
    it("returns the string as is", () => {
      expect(
        util.truncateStringAfterLength(1000, "some string below threshold")
      ).toEqual("some string below threshold");
    });
  });

  describe("when the string is on or above the threshold", () => {
    it("returns the truncated string", () => {
      const testInputs = [
        {
          threshold: 10,
          testString: "1234567890",
          expectedResult: "1234567...",
        },
        {
          threshold: 10,
          testString: "some string above threshold",
          expectedResult: "some st...",
        },
      ];

      testInputs.forEach(({ threshold, testString, expectedResult }) => {
        expect(util.truncateStringAfterLength(threshold, testString)).toEqual(
          expectedResult
        );
      });
    });
  });
});
