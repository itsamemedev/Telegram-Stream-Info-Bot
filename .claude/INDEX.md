# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (182)

```
 10432  GET              /                                                dashboard
 14397  GET              /api/abo/status                                  api_abo_status
 10505  GET              /api/active-recordings                           api_active_recordings
 14468  GET              /api/activity-pulse                              api_activity_pulse
 14275  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 21147  GET/POST         /api/audio/config                                api_audio_config
 21177  POST             /api/audio/testtone                              api_audio_testtone
 14341  GET/POST         /api/auto-archive-rules                          api_archive_rules
 14365  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 14369  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11957  GET              /api/automation/status                           api_automation_status
 11979  POST             /api/automation/toggle                           api_automation_toggle
 13206  GET              /api/azrael/agents                               api_azrael_agents
 11849  POST             /api/azrael/ask                                  api_azrael_ask
 21383  GET/POST         /api/azrael/context                              api_azrael_context
 12881  GET              /api/azrael/core                                 api_azrael_core
 21517  POST             /api/azrael/live_pause                           api_azrael_live_pause
 21507  GET              /api/azrael/live_status                          api_azrael_live_status
 21525  POST             /api/azrael/live_test                            api_azrael_live_test
 13215  GET              /api/azrael/memories                             api_azrael_memories
 21573  POST             /api/azrael/persona                              api_azrael_persona_set
 21564  GET              /api/azrael/personas                             api_azrael_personas
 21601  GET              /api/azrael/piper_status                         api_azrael_piper_status
 21356  POST             /api/azrael/react                                api_azrael_react
 21392  GET              /api/azrael/reaction                             api_azrael_reaction
 21544  GET              /api/azrael/reactions                            api_azrael_reactions
 21594  GET              /api/azrael/transcript                           api_azrael_transcript
 21479  POST             /api/azrael/tts_test                             api_azrael_tts_test
 21454  GET              /api/azrael/voices                               api_azrael_voices
 21618  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 10804  GET              /api/backoff-watch                               api_backoff_watch
 13756  POST             /api/backup/run                                  api_backup_run
 13722  GET              /api/backup/status                               api_backup_status
 13711  POST             /api/backup/system                               api_backup_system
 14307  GET              /api/bandwidth/live                              api_bandwidth_live
 14260  GET              /api/bookmarks                                   api_bookmarks_list
 11067  GET              /api/brain                                       api_brain
 11004  GET              /api/brain/alarms                                api_brain_alarms
 10989  GET              /api/brain/creator                               api_brain_creator
 10966  GET              /api/brain/graph                                 api_brain_graph
 11027  GET              /api/brain/growth                                api_brain_growth
  9982  GET              /api/brain/health                                api_brain_health
 22099  GET              /api/channel/categories                          api_channel_categories
 22105  POST             /api/channel/set                                 api_channel_set
 21915  GET              /api/channels/status                             api_channels_status
 20791  POST             /api/chat/send                                   api_chat_send
 13410  GET              /api/chat/send_status                            api_chat_send_status
 10486  GET              /api/checks                                      api_checks
 21420  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21403  GET              /api/clips                                       api_clips
 21436  POST/DELETE      /api/clips/clear                                 api_clips_clear
 21069  GET              /api/cohost                                      api_cohost
 21081  POST             /api/cohost/config                               api_cohost_config
 14776  GET              /api/community/stats                             api_community_stats
 22970  GET              /api/data/export                                 api_data_export
 20995  GET              /api/debug/threads                               api_debug_threads
 23797  GET              /api/defense/attacks                             api_defense_attacks
 23764  GET              /api/defense/crowdsec                            api_defense_crowdsec
 23782  GET              /api/defense/fail2ban                            api_defense_fail2ban
 23488  GET              /api/defense/overview                            api_defense_overview
 13818  POST             /api/discord/announce                            api_discord_announce
 13546  GET              /api/discord/clips_week                          api_discord_clips_week
 13762  GET              /api/discord/community                           api_discord_community
 13438  GET              /api/discord/invite                              api_discord_invite
 13012  GET              /api/discord/overview                            api_discord_overview
 13098  POST             /api/discord/webhook_test                        api_discord_webhook_test
 14289  GET              /api/events                                      api_events
 13593  GET              /api/events/stream                               api_events_stream
 14302  GET              /api/forecast/storage                            api_forecast_storage
 11995  GET              /api/freeai/status                               api_freeai_status
 12954  GET              /api/health                                      api_health
 14320  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 14316  GET              /api/heatmap/recordings                          api_heatmap_recordings
 21118  GET              /api/highlights                                  api_highlights
 21130  POST             /api/highlights/config                           api_highlights_config
 21956  GET              /api/kick/channel                                api_kick_channel
 21977  POST             /api/kick/channel                                api_kick_channel_set
 12681  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 12749  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 12727  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 12666  GET              /api/kick/oauth/start                            api_kick_oauth_start
 12706  GET              /api/kick/oauth/status                           api_kick_oauth_status
 21195  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 21264  POST             /api/kickmod/config                              api_kickmod_config
 21309  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 21323  GET              /api/kickmod/learned                             api_kickmod_learned
 21350  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 21330  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 21661  POST             /api/kickmod/say                                 api_kickmod_say
 21637  POST             /api/kickmod/start                               api_kickmod_start
 21235  GET              /api/kickmod/status                              api_kickmod_status
 21648  POST             /api/kickmod/stop                                api_kickmod_stop
 10366  POST             /api/login                                       dashboard_login_submit
 14761  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 14730  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13375  GET              /api/notify/status                               api_notify_status
 13386  POST             /api/notify/test                                 api_notify_test
 10590  GET              /api/outcomes                                    api_outcomes
 22576  POST             /api/overlay/config                              api_overlay_config
 22563  POST             /api/overlay/event                               api_overlay_event
 22468  GET              /api/overlay/state                               api_overlay_state
 10623  GET              /api/profile/<username>                          api_profile
 14486  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 14328  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 14451  GET              /api/proxy/heatmap                               api_proxy_heatmap
 14428  GET              /api/proxy/trend                                 api_proxy_trend
 12450  GET              /api/public/stats                                api_public_stats
 10466  GET              /api/pulse                                       api_pulse
 13896  GET              /api/recording-attempts                          api_recording_attempts
 20726  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 20704  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 20745  POST             /api/restream/<int:rid>/start                    api_restream_start
 21016  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 22430  GET              /api/restream/chatfeed                           api_restream_chatfeed
 20680  POST             /api/restream/create                             api_restream_create
 12757  GET              /api/restream/deck                               api_restream_deck
 11931  GET              /api/restream/health                             api_restream_health
 22452  POST             /api/restream/layout                             api_restream_layout
 20653  GET              /api/restream/list                               api_restream_list
 11900  POST             /api/restream/report                             api_restream_report
 21029  POST             /api/restream/start_all                          api_restream_start_all
 21055  POST             /api/restream/stop_all                           api_restream_stop_all
 12106  GET              /api/restream/testpush                           api_testpush_status
 12131  POST             /api/restream/testpush                           api_testpush_run
 14861  GET              /api/restream/verify                             api_restream_verify
 13524  GET              /api/retention/preview                           api_retention_preview
 13533  POST             /api/retention/run                               api_retention_run
 14245  GET              /api/search                                      api_search
 23535  GET              /api/selftest                                    api_selftest
 20762  GET              /api/shield/stats                                api_shield_stats
 10527  GET              /api/storage                                     api_storage
 10534  POST             /api/storage/cleanup                             api_storage_cleanup
 14382  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11870  GET              /api/stream/timeline                             api_stream_timeline
 13086  GET              /api/stream/transcript                           api_stream_transcript
 22718  GET              /api/streamer/compare                            api_streamer_compare
 22917  POST             /api/streamer/delete/<username>                  api_streamer_delete
 13485  GET              /api/streamer/detail                             api_streamer_detail
 22942  GET              /api/streamer/digest/<username>                  api_streamer_digest
 22822  GET              /api/streamer/dormant                            api_streamer_dormant
 22898  GET              /api/streamer/exists/<username>                  api_streamer_exists
 22777  GET              /api/streamer/journal/<username>                 api_streamer_journal
 22742  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 22802  GET              /api/streamer/watchlist                          api_streamer_watchlist
 12921  GET              /api/streamers/wall                              api_streamers_wall
 10558  GET              /api/summary/preview                             api_summary_preview
 13961  GET              /api/system                                      api_system
 14809  GET              /api/system/check_timing                         api_check_timing
 15132  GET              /api/system/config_drift                         api_config_drift
 13122  GET              /api/system/config_snapshot                      api_system_config_snapshot
 13233  GET              /api/system/preflight                            api_system_preflight
 13359  GET              /api/system/preflight_history                    api_system_preflight_history
 13658  GET              /api/system/resilience                           api_system_resilience
 14280  GET              /api/tags                                        api_tags_list
 10500  GET              /api/top                                         api_top
 10859  GET              /api/trend-7d                                    api_trend_7d
 21468  GET              /api/tts/<fn>                                    api_tts_file
 15104  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 15056  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect
 15080  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 15034  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 22604  GET              /api/upload_window                               api_upload_window
 10604  GET              /api/userstats                                   api_userstats
 12498  GET              /api/version                                     api_version
 14955  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 14976  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 14988  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout
 14913  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect
 14937  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 14891  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 27220  GET              /api/youtube/sendrate                            api_youtube_sendrate
 13934  GET              /archive/<int:eid>/download                      archive_download
 13991  GET              /download/<int:recording_id>                     download
 13874  GET              /health                                          health
 20964  GET              /healthz                                         healthz
 10357  GET              /login                                           dashboard_login_page
 10387  GET              /logout                                          dashboard_logout
 10394  GET              /manifest.webmanifest                            pwa_manifest
 13150  GET              /metrics                                         api_prometheus_metrics
 22413  GET              /overlay                                         overlay_page
 10418  GET              /pwa-icon-<variant>.png                          pwa_icon
 10404  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (173)

```
   176  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   146  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   986  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   726  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   857  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   837  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   875  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   799  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   339  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   350  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   360  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   383  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   390  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   401  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   534  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   632  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1224  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1256  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   323  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   939  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   919  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1092  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1140  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1191  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1050  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   894  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   358  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   622  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   504  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   487  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   479  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   315  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   331  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   666  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   631  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   651  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   538  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   265  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   250  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   173  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    51  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    58  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   194  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   221  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   181  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
    61  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
    94  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   102  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    42  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   118  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   148  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   133  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    73  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
    95  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   116  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
    63  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   163  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    27  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   182  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   202  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   229  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
    61  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
    86  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
    96  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    35  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    53  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   206  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
    83  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    49  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    60  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   125  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   120  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   111  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    36  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    75  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   250  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   317  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   345  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   196  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   263  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   498  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    63  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   161  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   144  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   384  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   815  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   897  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   925  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   936  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   802  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   864  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   851  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   832  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   477  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   472  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   520  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   403  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   730  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   494  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   457  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   430  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   704  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   574  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   663  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   569  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   502  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   282  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   747  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   370  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   625  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   780  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   765  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   326  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   564  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   550  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   533  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   590  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   683  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   579  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   306  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   296  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   331  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   109  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   200  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   195  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   255  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   219  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   434  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   463  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   383  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   396  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   492  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   369  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   244  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   289  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   300  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   146  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   258  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   116  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   350  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   405  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   104  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
    83  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   115  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
    96  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   446  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   412  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   471  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   451  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   434  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   427  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
```

## Discord-Slash-Commands (45)

```
 24240  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 24699  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 24331  /assign_role            Rolle/Gruppe einem Mitglied geben
 24377  /ban                    Mitglied bannen
 25031  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 24955  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 24995  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 24980  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 24822  /clips                  Letzte Highlight-Clips eines Users
 24292  /create_category        Kategorie anlegen
 24261  /create_channel         Text-Channel anlegen (optional in Kategorie)
 24320  /create_group           Nutzergruppe (= Rolle) anlegen
 24303  /create_role            Rolle / Nutzergruppe anlegen
 24277  /create_voice           Voice-Channel anlegen
 24613  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 24729  /event                  Community-Event ankündigen (Admin) — mit Countdown
 24772  /events                 Kommende Community-Events anzeigen
 24868  /follow                 Bei Live-Gang eines Streamers gepingt werden
 24852  /help                   Alle Bot-Befehle anzeigen
 24366  /kick                   Mitglied kicken
 24595  /leaderboard            Top-10 der Community nach XP
 24808  /livenow                Welche getrackten User sind gerade live
 24838  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 24669  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 24401  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 24581  /rank                   Dein Level und Rang anzeigen
 24795  /recstatus              Aktuell laufende Aufnahmen
 24342  /remove_role            Rolle/Gruppe entfernen
 24254  /restream_status        Restream-Status
 24353  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 24546  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 24564  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 24894  /stats                  Statistik zu einem getrackten Streamer
 24166  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 25190  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 25087  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 25063  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 24388  /timeout                Mitglied stummschalten (Minuten)
 24966  /topstreamers           Rangliste der Streamer nach Aufnahmen
 24196  /track                  TikTok-User tracken
 24180  /tracklist              Getrackte TikTok-User dieses Servers
 24883  /unfollow               Live-Pings für einen Streamer abbestellen
 24229  /untrack                TikTok-User nicht mehr tracken
 24916  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 24940  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 25674  on_member_join
 25636  on_message
 25277  on_raw_reaction_add
 25709  on_ready
```

## Top-Level-Symbole in bot.py (522 Funktionen, 2 Klassen)

```
  2479-2480   _abo_key
  2500-2518   _abo_probe_dump
 23077-23087  _active_recorder_sync
 17950-17957  _ad_allowlist
 19072-19078  _agent_for
 23089-23107  _ai_calls_total_sync
 19081-19097  _ai_telemetry
 19579-19597  _alert
 25822-25872  _alert_monitor_loop
 26251-26313  _announce_loop
  3421-3424   _anthropic_key
  3431-3433   _anthropic_model
 10110-10113  _arg_int
  2471-2476   _as_dict
 15810-15815  _audio_cfg
 19733-19755  _audio_tap_cmd
 10278-10289  _auth_cookie
 10245-10274  _auth_guard
  1627-1632   _auto_on
 20629-20647  _auto_restream_loop
 27381-27396  _azrael_broadcast_reply
 27281-27303  _azrael_chat_reply
 27264-27278  _azrael_chat_should_reply
 27309-27311  _azrael_gate_cfg
 19102-19116  _azrael_live_state
 22316-22330  _azrael_overlay_state
 19462-19516  _azrael_proactive_loop
 18921-18977  _azrael_reaction_to_chats
 27314-27321  _azrael_reply_all_chats
 27251-27261  _azrael_self_names
 27349-27378  _azrael_send_to
 19119-19140  _azrael_system
 25991-25994  _backup_active
 26072-26085  _backup_loop
 17838-17839  _badwords_path
 25787-25796  _brain_growth_loop
 10935-10962  _brain_growth_snapshot
  2407-2427   _brain_hint_delay
 10927-10929  _brain_history_for
  6510-6538   _brain_notify
 10904-10925  _brain_record
 10931-10933  _brain_stream_recent
 13572-13589  _browser_push
  6554-6641   _build_daily_summary
  2910-3090   _build_native_cmd
 16158-16345  _build_restream_cmd
  3134-3167   _build_ytdlp_cmd
 23029-23036  _cached_probe
  5332-5359   _can_stop_tracking
  1807-1829   _capture_set_cookies
 14545-14548  _cfg_get
 14551-14553  _cfg_set
 22060-22095  _channel_set_all
 15408-15411  _chat_connected
 15414-15430  _chat_disconnected
  8590-8601   _chat_is_forum
 15450-15452  _chat_sanitize
 15454-15463  _chat_src_ok
 15393-15405  _chat_stat
 15433-15436  _chat_stats_snapshot
  3696-3707   _check_ai_alive_sync
  3710-3722   _check_ai_models_sync
 23038-23051  _check_redis_alive_sync
 23053-23073  _check_redis_version_sync
 13450-13463  _ci_key
 11534-11577  _classify_pool_anonymity
 11580-11597  _classify_pool_anonymity_bg
   785-789    _claude_chat_sync_metered
 10139-10146  _client_ip
 26345-26372  _clip_prune
 26375-26385  _clip_recfile_for
 26901-26907  _clip_should_velocity
 26426-26508  _clip_to_discord
  3594-3603   _close_ai_session
 27425-27440  _cohost_broadcast
 27407-27411  _cohost_cfg
 27466-27478  _cohost_fire_highlight
 27414-27422  _cohost_gate
 27443-27463  _cohost_highlight
 26557-26591  _community_events_loop
 10758-10760  _conv_messages
  6940-6980   _cookie_alarm_loop
  1879-1883   _cookie_autorefresh_info
  1784-1788   _cookie_header
 13622-13654  _cpu_load_snapshot
  3904-3916   _create_index_safe
 23290-23396  _crowdsec_status
 23256-23287  _crowdsec_via_lapi
 23121-23139  _cscli_bin
 23145-23158  _cscli_path
  6833-6858   _daily_summary_loop
 23176-23193  _darf_journal_lesen
 25799-25819  _db_maintenance_loop
  6802-6830   _db_vacuum_loop
 17973-17997  _detect_foreign_ad
  1365-1376   _diag_path_owner
 19368-19412  _director_finalize
 20179-20186  _director_for
 19317-19365  _director_mark
 26795-26830  _disc_automod_check
 26768-26774  _disc_state_get
 26777-26784  _disc_state_set
 23839-23852  _discord_guild_filesize_bytes
 24038-24047  _discord_invite
 26729-26765  _discord_live_thread
 19519-19531  _discord_notify
 23939-23964  _discord_ops_alert
 26627-26725  _discord_post_user
 24103-25784  _discord_run_once
 23977-24035  _discord_start
 26316-26322  _discord_stop
 23860-23862  _discord_upload_limit_label
 23855-23857  _discord_upload_limit_mb
  6861-6935   _disk_alarm_loop
 28827-28876  _disk_autoclean
 28879-28892  _disk_guard_loop
 28819-28824  _disk_pct
 15767-15769  _drawtext_chain
 14088-14090  _dump_all_threads
 11459-11523  _enrich_proxies_with_geo
  2024-2068   _ensure_cookie_file_netscape
 24050-24100  _ensure_discord_invite
 26522-26554  _ensure_error_channel
  8649-8652   _ensure_notify_topic
 11702-11739  _ensure_proxy_ready
  8603-8630   _ensure_topic
   648-650    _env_int
   653-655    _env_int_range
 26594-26624  _error_channel_loop
 19563-19576  _event_webhook
 15219-15229  _evolution_loop
  5952-5986   _extract_file_payload
  2156-2158   _extract_urls_from_streamurl_node
 23161-23168  _f2b_sudo_hint
 19599-19601  _faster_whisper_available
 17862-17874  _fetch_ldnoobw_de
 11348-11366  _fetch_proxy_list
 20013-20041  _fetch_tiktok_room_id
   719-722    _ff_cmd
 15930-15935  _find_chromium
  3127-3131   _find_external_recorder
  2161-2163   _find_stream_urls
 14596-14621  _fire_webhooks
  7716-7725   _fork_safe
   800-809    _freeai_chat_sync_metered
 23211-23253  _geo_lookup_ips
  3583-3592   _get_ai_session
  7550-7590   _get_live_info
  2697-2704   _get_resolve_semaphore
  7951-8317   _handle_single_tracking
 28671-28673  _hb
 28676-28693  _hb_while
 15468-15470  _highlight_cfg
 15473-15502  _highlight_observe
 15938-15943  _htmlov_screenshot_cmd
 19757-19767  _httpx_proxy
 14629-14641  _in_quiet_hours
 29706-29737  _install_fast_eventloop
 10005-10059  _install_fast_json
 14093-14109  _install_faulthandler
 20872-20881  _intel_ensure_schema
 20919-20954  _intel_index_loop
 20893-20903  _intel_index_one
 20884-20890  _intel_semantic
  5321-5330   _is_authorized
  7881-7887   _is_dead
  2146-2148   _is_hevc
 23196-23202  _is_private_ip
  1529-1536   _is_process_running
  6540-6551   _is_quiet_hours
  1166-1175   _is_upload_window
 10094-10107  _json_error_handler
  6760-6790   _kick_broadcaster_id
 12032-12051  _kick_channel_live
  6674-6716   _kick_follower_count
 12644-12657  _kick_oauth_exchange
 12660-12662  _kick_oauth_page
 12603-12607  _kick_redirect_public
 12598-12600  _kick_redirect_source
 12590-12595  _kick_redirect_uri
  6659-6661   _kick_slug
 12610-12641  _kick_user_token
  3953-3956   _kind_from_filename
 14658-14663  _latest_popularity
 17884-17890  _learned_load
 17881-17882  _learned_path
 17892-17900  _learned_save
 20394-20424  _live_react_loop
 20190-20383  _live_react_worker
 18980-18991  _live_transcript_push
 20385-20392  _live_users
 19415-19459  _living_title_loop
 17841-17849  _load_banned_words_file
  1705-1778   _load_cookies_dict
 25997-26069  _local_backup_scan
 10076-10090  _log_5xx
 16353-16365  _looks_like_codec_err
 16348-16350  _looks_like_source_expired
  7797-7827   _loop_fehler
 14113-14122  _loop_heartbeat
 28641-28668  _loop_lag_monitor
 14125-14193  _loop_watchdog_thread
 18860-18874  _loyalty_add
 18851-18857  _loyalty_get
 18877-18885  _loyalty_top
 14795-14797  _manual_donations_total
  7889-7890   _mark_dead
 12203-12219  _marketing_loop
 27328-27346  _maybe_handle_command
 28978-29002  _maybe_hype_clip
  3871-3894   _migrate_columns
 27605-27616  _mod_is_exempt
 27619-27624  _mod_warn_first
 27627-27630  _mod_warn_text
 15256-15264  _modlog
   919-921    _multistream_targets
  7728-7729   _nc_create_subprocess_exec
  7732-7733   _nc_create_subprocess_shell
 12455-12472  _news_loop
 15294-15296  _normalize_ingest
  2338-2355   _note_check_duration
  8643-8646   _notify_topic_name
 12554-12565  _oauth_redirect_env
 12581-12587  _oauth_redirect_source
 12568-12578  _oauth_redirect_uri
 19006-19014  _oracle_memories
 19272-19306  _oracle_memorize
 19017-19030  _oracle_persona
 18999-19003  _oracle_recent_text
 15593-15601  _ov_atomic_write
 15581-15587  _ov_bar
 17797-17809  _ov_clip_text
 15590-15591  _ov_oneline
 22380-22409  _overlay_push
 15884-15927  _overlay_render_size
 15355-15359  _overlay_session_reset
 22332-22335  _overlay_src_ok
 17960-17970  _own_invites
 15879-15881  _parse_size
 23404-23484  _parse_ssh_attacks
  7152-7185   _pause_resume_cmd
  1833-1877   _persist_refreshed_cookies
  1671-1703   _pick_checked_pull_proxy
 10175-10188  _pin_auth_value
 10234-10235  _pin_clear_fail
 10214-10217  _pin_locked
 10220-10231  _pin_note_fail
 10191-10211  _pin_ok
 22222-22224  _piper_available
 22187-22209  _piper_list_voices
 22229-22254  _piper_pick_model
 22266-22313  _piper_say
 22180-22184  _piper_voice_roots
 14558-14593  _post_json_threaded
 15858-15876  _probe_video_size
  1557-1574   _proc_is_recorder
 11446-11457  _proxy_geo_cache_put
 11673-11699  _proxy_pool_refresh_loop
  1637-1668   _proxy_report_recording
 14078-14080  _prune_stall_dumps
 12513-12551  _public_base_url
 12273-12394  _public_stats
 19534-19560  _push_notify
 10336-10338  _pwa_dir
 11417-11432  _quick_validate_proxy
 14624-14626  _quiet_hours_config
 10301-10334  _rate_guard
 18825-18831  _react_warn
  7636-7675   _reap_proc
  2378-2400   _record_check_outcome
   714-716    _redact_stream_urls
 11600-11670  _refresh_proxy_pool
 22212-22218  _resolve_piper_model
 13466-13481  _resolve_tracked_user
  2172-2262   _resolve_via_html
  2520-2674   _resolve_via_webcast_api_v2
  2737-2799   _resolve_via_ytdlp
 26947-27076  _resolve_youtube_ingest
 20463-20470  _restream_active_platforms
 15340-15351  _restream_active_sources
 20044-20143  _restream_chat_guardian
 15505-15577  _restream_chat_push
 15267-15279  _restream_enabled
 15946-16033  _restream_html_overlay_start
 16036-16049  _restream_html_overlay_stop
  1114-1116   _restream_layout_mode
 15305-15328  _restream_overlay_files
 20428-20460  _restream_platform_state
 20591-20626  _restream_resume_after_restart
 16097-16155  _restream_tts_enqueue_wav
 15820-15852  _restream_tts_feeder
 15817-15818  _restream_tts_fifo_path
 16052-16079  _restream_tts_start
 16081-16095  _restream_tts_stop
 20473-20588  _restream_verify_loop
 25962-25974  _retention_loop
 25921-25959  _retention_scan
  2482-2484   _room_is_abo
  5990-6107   _run_ai_call
 14216-14229  _run_async_from_flask
 23205-23208  _run_priv
 29694-29702  _run_selfcheck_and_exit
 25977-25988  _s3_client
  7892-7938   _safe_send
  4585-4601   _sample_net_throughput
 17851-17859  _save_banned_words_file
  2430-2457   _schedule_next_check
 25875-25918  _scheduler_loop
  3897-3901   _schema_pk
 14233-14238  _scraper_session
 27633-27672  _screen_full
 12970-13007  _sec_headers
  2151-2153   _select_stream_from_data_section
 29507-29691  _selfcheck
  8655-8689   _send_live_notice
  1189-1193   _should_defer_upload
 26388-26423  _shrink_for_discord
 10341-10353  _sicheres_ziel
 28899-28916  _sign_health_check
 28919-28938  _sign_health_loop
  7745-7756   _spawn
  7759-7789   _spawn_from_flask
 23528-23531  _st_befund
 19769-20010  _start_chat_listener
 14196-14213  _start_loop_watchdog
 12418-12446  _stats_loop
 12397-12400  _stats_output_path
 12403-12415  _stats_write
  8385-8399   _storage_cleanup_loop
 28958-28965  _story_for
  3189-3195   _stream_url_expiry
  3204-3210   _stream_url_is_fresh
  3197-3202   _stream_url_ttl
 17924-17931  _streamer_persona_get
 17906-17912  _streamer_personas_load
 17903-17904  _streamer_personas_path
 17914-17922  _streamer_personas_save
 15772-15776  _studio_chain
 26094-26216  _system_backup
 26219-26247  _system_backup_loop
 11369-11408  _test_proxy
 12073-12082  _testpush_cfg
 12085-12102  _testpush_exec
 12054-12070  _testpush_resolve_live
  8562-8572   _tg_topics_load_into_mem
  8559-8560   _tg_topics_path
  8574-8581   _tg_topics_save
 22846-22894  _tiktok_account_exists
 10149-10157  _token_ok
  8584-8588   _topic_forget
 14644-14655  _tracking_max_duration
  4203-4215   _tracking_resume_cleanup
  1423-1446   _try_attach_file_handler
 22256-22264  _tts_cleanup
 12010-12014  _tunnel_effective
 21682-21735  _twitch_channel_status
 27675-27818  _twitch_chat_loop
 27489-27592  _twitch_eventsub_loop
 15125-15128  _twitch_oauth_page
  1212-1225   _upload_queue_add
  1236-1238   _upload_queue_count
  1195-1204   _upload_queue_load
  1185-1187   _upload_queue_path
  1227-1234   _upload_queue_remove
  1206-1210   _upload_queue_save
  1240-1281   _upload_window_loop
  7609-7616   _uptime_s
 15282-15291  _url_host
   694-711    _url_ohne_zugang
   778-782    _usage_record_claude
  7830-7874   _verbindung_verloren
  6719-6750   _viewer_sample_loop
  6792-6799   _viewer_stats
 10238-10241  _wants_html
  7619-7633   _warn_empty_env
 28714-28809  _watchdog_loop
 27230-27238  _wchat_thank_ok
 19603-19633  _whisper_get_model
  7706-7713   _whisper_native_section
 18812-18818  _whisper_pool
 19702-19731  _whisper_segments
 19635-19699  _whisper_transcribe
 15603-15765  _write_restream_overlay
 27846-27925  _youtube_api_chat_loop
 21738-21841  _youtube_api_status
 21844-21911  _youtube_channel_status
 27928-28088  _youtube_chat_loop
 27082-27095  _youtube_restream_autoconfig
 27098-27122  _youtube_restream_autoconfig_inner
 27188-27216  _youtube_send
 22016-22057  _youtube_set_channel
 27125-27159  _yt_access_token
 27162-27177  _yt_live_chat_id
 27839-27843  _yt_oauth_configured
 27183-27185  _yt_sendrate_cfg
 27821-27836  _yt_timeout
  2721-2722   _ytdlp_detect_available
  2724-2735   _ytdlp_note_result
 14083-14085  _zombie_child_count
  7486-7510   about
  4072-4076   add_ai_log_entry
  3989-3992   add_archive_entry
  4698-4713   add_archive_rule
  4374-4408   add_recording
  4137-4154   add_tracking
  6110-6143   ai
  3736-3775   ai_chat
  3809-3819   ai_history_append
  3821-3826   ai_history_clear
  3798-3807   ai_history_load
  3783-3796   ai_rate_limit_check
  6172-6180   aireset
 19143-19162  azrael_chat
 28093-28215  brain_cmd
  3213-3397   build_recording_cmd
  4157-4160   bulk_add_trackings
  6983-7042   bulkadd
  8402-8542   check_all_trackings
  4219-4231   claim_live_transition
 18000-18755  class KickModerator
 16368-17684  class RestreamManager
 11784-11826  classify_proxy_anonymity
  6218-6416   cleanup
  5181-5222   cleanup_old_recordings
  4365-4372   clear_recording
 26833-26898  clip_moment
  4529-4578   compute_storage_forecast
  7105-7149   cookies_cmd
  4128-4134   count_trackings_for_chat
  4059-4070   decide_preferred_recorder
  3999-4002   delete_archive_entry
  4715-4723   delete_archive_rule
  5647-5794   diag
 28327-28388  einnahmen_cmd
  4523-4526   find_recordings_by_fingerprint
  4020-4036   finish_recording_attempt
  4191-4193   get_all_active_trackings
  4087-4090   get_all_checks
  4410-4413   get_all_recordings
  4472-4474   get_all_tags_with_counts
  4500-4503   get_annotations_for_recording
  3994-3997   get_archive_entry
  4493-4496   get_bookmarked_recordings
  1900-2017   get_cookie_health
  4460-4466   get_event_log
  4043-4057   get_last_recording_attempt
  2802-2907   get_live_status
  4981-4984   get_manual_recordings
  4508-4511   get_or_compute_inspect_sync
  5257-5301   get_outcome_breakdown
  4479-4482   get_priority_poll_interval
  4676-4685   get_profile_snapshots
  4038-4041   get_recent_recording_attempts
  4415-4418   get_recording_by_id
  4486-4489   get_recording_note
  3531-3554   get_redis
  4117-4120   get_stats
  5148-5179   get_storage_stats
  4816-4818   get_tiktok_status_distribution
  4233-4242   get_tracking_state
  4188-4189   get_trackings_for_group
  4997-5000   get_trash_recordings
  9310-9973   handle_recording_finished
  3919-3944   init_db
  5071-5125   inspect_stream_url
 22375-22377  is_revenue_platform
  4688-4696   list_archive_rules
  5451-5489   live
  7941-7949   live_check_worker
  3606-3640   llm_chat
  3663-3691   llm_chat_sync
  3648-3660   llm_list_models
  4426-4452   log_event
  1491-1524   log_recording_failure
  7299-7348   logs_cmd
 29006-29497  main
  6146-6169   on_ai_media
  7425-7451   on_ai_reply
  7454-7483   on_azrael_mention
  7515-7545   on_callback
 19165-19269  oracle_handle
  7188-7191   pause_tracking
  5311-5316   profile_keyboard
  7250-7296   quota
  8319-8382   reaper_loop
  4812-4814   record_tiktok_status
  6185-6215   recstatus
  3556-3564   redis_get_json
  3566-3572   redis_set_json
  4162-4186   remove_tracking
 28391-28401  report_cmd
 11829-11831  report_proxy_result
  2265-2292   resolve_tiktok_live_stream
  4992-4995   restore_recording
  7194-7197   resume_tracking
  4726-4806   run_archive_rules
 28404-28621  run_bot
 14005-14052  run_flask
  4604-4649   sample_bandwidth_for_active
  4655-4674   save_profile_snapshot
  4079-4085   save_tiktok_check
  4357-4363   set_recording_file
  4196-4200   set_tracking_paused
  4987-4990   soft_delete_recording
  8695-9308   split_and_send_video
  5364-5406   start
  4004-4018   start_recording_attempt
  6419-6457   stats
  4962-4979   stop_manual_recording
  7200-7247   stoprec
  6644-6652   summary_cmd
  7351-7422   sysres
  5796-5940   teststream
  5408-5449   tiktok
  7045-7102   topusers
  5526-5583   track
  5491-5523   track_exact
  5597-5645   tracklist
  4828-4960   trigger_manual_recording
  4318-4355   try_acquire_recording_lock
  5003-5062   universal_search
  5585-5595   untrack
 28218-28324  update_cmd
  4518-4521   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
persona.py             —
piper_voices.py        resolve_model_path, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       looks_like_source_expired, normalize_ingest
restrend.py            rising_trend
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
trackingdb.py          add_tracking_tag, bulk_add_trackings, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking_tag, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                —
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
