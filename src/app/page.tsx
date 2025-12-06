export default function Home() {
  return (
    <div className="max-w-4xl mx-auto px-6 pb-16">
      <div className="grid md:grid-cols-2 gap-16">
        <section>
          <h2 className="text-2xl font-medium text-white mb-8">Experience</h2>
          
          <div className="space-y-6">
            <div>
              <div className="flex justify-between items-start mb-1">
                <div>
                  <h3 className="text-white font-medium">Chainlink Labs</h3>
                  <p className="text-gray-400 text-sm">senior engineer</p>
                </div>
                <span className="text-gray-500 text-sm">2023 -</span>
              </div>
            </div>

            <div>
              <div className="flex justify-between items-start mb-1">
                <div>
                  <h3 className="text-white font-medium">AWS</h3>
                  <p className="text-gray-400 text-sm">software engineer, AWS cryptography</p>
                </div>
                <span className="text-gray-500 text-sm">2021 - 2023</span>
              </div>
            </div>

            <div>
              <div className="flex justify-between items-start mb-1">
                <div>
                  <h3 className="text-white font-medium">BanklessDAO</h3>
                  <p className="text-gray-400 text-sm">lead engineer + product</p>
                </div>
                <span className="text-gray-500 text-sm">2021 - 2023</span>
              </div>
            </div>

            <div>
              <div className="flex justify-between items-start mb-1">
                <div>
                  <h3 className="text-white font-medium">A-Level Capital</h3>
                  <p className="text-gray-400 text-sm">managing partner</p>
                </div>
                <span className="text-gray-500 text-sm">2018 - 2021</span>
              </div>
            </div>
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-medium text-white mb-8">Projects</h2>

          <div>
          <a href="https://www.prnewswire.com/news-releases/chainlink-runtime-environment-goes-live-unlocking-institutional-tokenization-at-scale-302604067.html" target="_blank" rel="noopener noreferrer" className="group"></a>  
              <h3 className="text-white font-medium mb-1">Chainlink Runtime Environment (CRE)</h3>
              <p className="text-gray-400 text-sm">
                built and launched developer platform for web2 developers to use web3 capabilities. 
              </p>
            </div>
          
          <div className="space-y-6">
            <div>
            <a href="https://aws.amazon.com/iam/roles-anywhere/" target="_blank" rel="noopener noreferrer" className="group">
                <h3 className="text-white font-medium mb-1 group-hover:text-gray-300 transition-colors">AWS IAM RolesAnywhere</h3>
                <p className="text-gray-400 text-sm">
                  built and launched AWS authentication service for on-prem workfloads
                </p>
              </a>
            </div>

            <div>
              <a href="https://github.com/BanklessDAO/bounty-board" target="_blank" rel="noopener noreferrer" className="group">
                <h3 className="text-white font-medium mb-1 group-hover:text-gray-300 transition-colors">Bounty Board</h3>
                <p className="text-gray-400 text-sm">
                  built and launched a discord/web job board with bounties for community contributions
                </p>
              </a>
            </div>

          </div>
        </section>
      </div>
    </div>
  );
}
