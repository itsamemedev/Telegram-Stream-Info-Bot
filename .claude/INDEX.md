# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (172)

```
 10472  GET              /                                                dashboard
 14343  GET              /api/abo/status                                  api_abo_status
 10545  GET              /api/active-recordings                           api_active_recordings
 14414  GET              /api/activity-pulse                              api_activity_pulse
 14221  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 21099  GET/POST         /api/audio/config                                api_audio_config
 21129  POST             /api/audio/testtone                              api_audio_testtone
 14287  GET/POST         /api/auto-archive-rules                          api_archive_rules
 14311  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 14315  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11999  GET              /api/automation/status                           api_automation_status
 12021  POST             /api/automation/toggle                           api_automation_toggle
 13218  GET              /api/azrael/agents                               api_azrael_agents
 11891  POST             /api/azrael/ask                                  api_azrael_ask
 21335  GET/POST         /api/azrael/context                              api_azrael_context
 12923  GET              /api/azrael/core                                 api_azrael_core
 21469  POST             /api/azrael/live_pause                           api_azrael_live_pause
 21459  GET              /api/azrael/live_status                          api_azrael_live_status
 21477  POST             /api/azrael/live_test                            api_azrael_live_test
 13227  GET              /api/azrael/memories                             api_azrael_memories
 21525  POST             /api/azrael/persona                              api_azrael_persona_set
 21516  GET              /api/azrael/personas                             api_azrael_personas
 21553  GET              /api/azrael/piper_status                         api_azrael_piper_status
 21308  POST             /api/azrael/react                                api_azrael_react
 21344  GET              /api/azrael/reaction                             api_azrael_reaction
 21496  GET              /api/azrael/reactions                            api_azrael_reactions
 21546  GET              /api/azrael/transcript                           api_azrael_transcript
 21431  POST             /api/azrael/tts_test                             api_azrael_tts_test
 21406  GET              /api/azrael/voices                               api_azrael_voices
 21570  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 10844  GET              /api/backoff-watch                               api_backoff_watch
 13702  POST             /api/backup/run                                  api_backup_run
 13668  GET              /api/backup/status                               api_backup_status
 13657  POST             /api/backup/system                               api_backup_system
 14253  GET              /api/bandwidth/live                              api_bandwidth_live
 14206  GET              /api/bookmarks                                   api_bookmarks_list
 11107  GET              /api/brain                                       api_brain
 11044  GET              /api/brain/alarms                                api_brain_alarms
 11029  GET              /api/brain/creator                               api_brain_creator
 11006  GET              /api/brain/graph                                 api_brain_graph
 11067  GET              /api/brain/growth                                api_brain_growth
 10022  GET              /api/brain/health                                api_brain_health
 22051  GET              /api/channel/categories                          api_channel_categories
 22057  POST             /api/channel/set                                 api_channel_set
 21867  GET              /api/channels/status                             api_channels_status
 20743  POST             /api/chat/send                                   api_chat_send
 13422  GET              /api/chat/send_status                            api_chat_send_status
 10526  GET              /api/checks                                      api_checks
 21372  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21355  GET              /api/clips                                       api_clips
 21388  POST/DELETE      /api/clips/clear                                 api_clips_clear
 21021  GET              /api/cohost                                      api_cohost
 21033  POST             /api/cohost/config                               api_cohost_config
 14722  GET              /api/community/stats                             api_community_stats
 22691  GET              /api/data/export                                 api_data_export
 20947  GET              /api/debug/threads                               api_debug_threads
 23518  GET              /api/defense/attacks                             api_defense_attacks
 23485  GET              /api/defense/crowdsec                            api_defense_crowdsec
 23503  GET              /api/defense/fail2ban                            api_defense_fail2ban
 23209  GET              /api/defense/overview                            api_defense_overview
 13764  POST             /api/discord/announce                            api_discord_announce
 13492  GET              /api/discord/clips_week                          api_discord_clips_week
 13708  GET              /api/discord/community                           api_discord_community
 13450  GET              /api/discord/invite                              api_discord_invite
 13024  GET              /api/discord/overview                            api_discord_overview
 13110  POST             /api/discord/webhook_test                        api_discord_webhook_test
 14235  GET              /api/events                                      api_events
 13539  GET              /api/events/stream                               api_events_stream
 14248  GET              /api/forecast/storage                            api_forecast_storage
 12037  GET              /api/freeai/status                               api_freeai_status
 12966  GET              /api/health                                      api_health
 14266  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 14262  GET              /api/heatmap/recordings                          api_heatmap_recordings
 21070  GET              /api/highlights                                  api_highlights
 21082  POST             /api/highlights/config                           api_highlights_config
 21908  GET              /api/kick/channel                                api_kick_channel
 21929  POST             /api/kick/channel                                api_kick_channel_set
 12723  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 12791  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 12769  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 12708  GET              /api/kick/oauth/start                            api_kick_oauth_start
 12748  GET              /api/kick/oauth/status                           api_kick_oauth_status
 21147  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 21216  POST             /api/kickmod/config                              api_kickmod_config
 21261  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 21275  GET              /api/kickmod/learned                             api_kickmod_learned
 21302  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 21282  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 21613  POST             /api/kickmod/say                                 api_kickmod_say
 21589  POST             /api/kickmod/start                               api_kickmod_start
 21187  GET              /api/kickmod/status                              api_kickmod_status
 21600  POST             /api/kickmod/stop                                api_kickmod_stop
 10406  POST             /api/login                                       dashboard_login_submit
 14707  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 14676  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13387  GET              /api/notify/status                               api_notify_status
 13398  POST             /api/notify/test                                 api_notify_test
 10630  GET              /api/outcomes                                    api_outcomes
 22528  POST             /api/overlay/config                              api_overlay_config
 22515  POST             /api/overlay/event                               api_overlay_event
 22420  GET              /api/overlay/state                               api_overlay_state
 10663  GET              /api/profile/<username>                          api_profile
 14432  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 14274  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 14397  GET              /api/proxy/heatmap                               api_proxy_heatmap
 14374  GET              /api/proxy/trend                                 api_proxy_trend
 12492  GET              /api/public/stats                                api_public_stats
 10506  GET              /api/pulse                                       api_pulse
 13842  GET              /api/recording-attempts                          api_recording_attempts
 20678  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 20656  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 20697  POST             /api/restream/<int:rid>/start                    api_restream_start
 20968  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 22382  GET              /api/restream/chatfeed                           api_restream_chatfeed
 20632  POST             /api/restream/create                             api_restream_create
 12799  GET              /api/restream/deck                               api_restream_deck
 11973  GET              /api/restream/health                             api_restream_health
 22404  POST             /api/restream/layout                             api_restream_layout
 20605  GET              /api/restream/list                               api_restream_list
 11942  POST             /api/restream/report                             api_restream_report
 20981  POST             /api/restream/start_all                          api_restream_start_all
 21007  POST             /api/restream/stop_all                           api_restream_stop_all
 12148  GET              /api/restream/testpush                           api_testpush_status
 12173  POST             /api/restream/testpush                           api_testpush_run
 14807  GET              /api/restream/verify                             api_restream_verify
 13470  GET              /api/retention/preview                           api_retention_preview
 13479  POST             /api/retention/run                               api_retention_run
 14191  GET              /api/search                                      api_search
 23256  GET              /api/selftest                                    api_selftest
 20714  GET              /api/shield/stats                                api_shield_stats
 10567  GET              /api/storage                                     api_storage
 10574  POST             /api/storage/cleanup                             api_storage_cleanup
 14328  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11912  GET              /api/stream/timeline                             api_stream_timeline
 13098  GET              /api/stream/transcript                           api_stream_transcript
 10598  GET              /api/summary/preview                             api_summary_preview
 13907  GET              /api/system                                      api_system
 14755  GET              /api/system/check_timing                         api_check_timing
 15078  GET              /api/system/config_drift                         api_config_drift
 13134  GET              /api/system/config_snapshot                      api_system_config_snapshot
 13245  GET              /api/system/preflight                            api_system_preflight
 13371  GET              /api/system/preflight_history                    api_system_preflight_history
 13604  GET              /api/system/resilience                           api_system_resilience
 14226  GET              /api/tags                                        api_tags_list
 10540  GET              /api/top                                         api_top
 10899  GET              /api/trend-7d                                    api_trend_7d
 21420  GET              /api/tts/<fn>                                    api_tts_file
 15050  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 15002  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect
 15026  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 14980  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 22556  GET              /api/upload_window                               api_upload_window
 10644  GET              /api/userstats                                   api_userstats
 12540  GET              /api/version                                     api_version
 14901  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 14922  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 14934  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout
 14859  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect
 14883  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 14837  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 26967  GET              /api/youtube/sendrate                            api_youtube_sendrate
 13880  GET              /archive/<int:eid>/download                      archive_download
 13937  GET              /download/<int:recording_id>                     download
 13820  GET              /health                                          health
 20916  GET              /healthz                                         healthz
 10397  GET              /login                                           dashboard_login_page
 10427  GET              /logout                                          dashboard_logout
 10434  GET              /manifest.webmanifest                            pwa_manifest
 13162  GET              /metrics                                         api_prometheus_metrics
 22365  GET              /overlay                                         overlay_page
 10458  GET              /pwa-icon-<variant>.png                          pwa_icon
 10444  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (187)

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
    57  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    46  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   204  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    70  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
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
   109  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   256  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    71  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   281  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   213  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   237  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   168  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   133  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   193  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    39  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
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
 23982  /ai                     
 24441  /ask                    
 24073  /assign_role            
 24119  /ban                    
 24773  /botstats               
 24697  /clearwarns             
 24737  /clip                   
 24722  /clipoftheweek          
 24564  /clips                  
 24034  /create_category        
 24003  /create_channel         
 24062  /create_group           
 24045  /create_role            
 24019  /create_voice           
 24355  /daily                  
 24471  /event                  
 24514  /events                 
 24610  /follow                 
 24594  /help                   
 24108  /kick                   
 24337  /leaderboard            
 24550  /livenow                
 24580  /post_test              
 24411  /profile                
 24143  /purge                  
 24323  /rank                   
 24537  /recstatus              
 24084  /remove_role            
 23996  /restream_status        
 24095  /set_channel_perms      
 24288  /setup_community        
 24306  /setup_targets          
 24636  /stats                  
 23908  /status                 
 24932  /streaminfo             
 24829  /sys_report             
 24805  /sys_unpause            
 24130  /timeout                
 24708  /topstreamers           
 23938  /track                  
 23922  /tracklist              
 24625  /unfollow               
 23971  /untrack                
 24658  /warn                   
 24682  /warnings               
```

## Discord-Events (4)

```
 25416  on_member_join
 25378  on_message
 25019  on_raw_reaction_add
 25451  on_ready
```

## Top-Level-Symbole in bot.py (520 Funktionen, 2 Klassen)

```
  2488-2489   _abo_key
  2509-2527   _abo_probe_dump
 22798-22808  _active_recorder_sync
 17899-17906  _ad_allowlist
 19021-19027  _agent_for
 22810-22828  _ai_calls_total_sync
 19030-19046  _ai_telemetry
 19528-19546  _alert
 25567-25617  _alert_monitor_loop
 25998-26060  _announce_loop
  3430-3433   _anthropic_key
  3440-3442   _anthropic_model
 10150-10153  _arg_int
  2480-2485   _as_dict
 15759-15764  _audio_cfg
 19682-19704  _audio_tap_cmd
 10318-10329  _auth_cookie
 10285-10314  _auth_guard
  1636-1641   _auto_on
 20581-20599  _auto_restream_loop
 27128-27143  _azrael_broadcast_reply
 27028-27050  _azrael_chat_reply
 27011-27025  _azrael_chat_should_reply
 27056-27058  _azrael_gate_cfg
 19051-19065  _azrael_live_state
 22268-22282  _azrael_overlay_state
 19411-19465  _azrael_proactive_loop
 18870-18926  _azrael_reaction_to_chats
 27061-27068  _azrael_reply_all_chats
 26998-27008  _azrael_self_names
 27096-27125  _azrael_send_to
 19068-19089  _azrael_system
 25736-25739  _backup_active
 25817-25830  _backup_loop
 17787-17788  _badwords_path
 25529-25538  _brain_growth_loop
 10975-11002  _brain_growth_snapshot
  2416-2436   _brain_hint_delay
 10967-10969  _brain_history_for
  6509-6537   _brain_notify
 10944-10965  _brain_record
 10971-10973  _brain_stream_recent
 13518-13535  _browser_push
  6553-6640   _build_daily_summary
  2919-3099   _build_native_cmd
 16107-16294  _build_restream_cmd
  3143-3176   _build_ytdlp_cmd
 22750-22757  _cached_probe
  5331-5358   _can_stop_tracking
  1816-1838   _capture_set_cookies
 14491-14494  _cfg_get
 14497-14499  _cfg_set
 22012-22047  _channel_set_all
 15357-15360  _chat_connected
 15363-15379  _chat_disconnected
  8630-8641   _chat_is_forum
 15399-15401  _chat_sanitize
 15403-15412  _chat_src_ok
 15342-15354  _chat_stat
 15382-15385  _chat_stats_snapshot
  3705-3716   _check_ai_alive_sync
  3719-3731   _check_ai_models_sync
 22759-22772  _check_redis_alive_sync
 22774-22794  _check_redis_version_sync
 11574-11617  _classify_pool_anonymity
 11620-11637  _classify_pool_anonymity_bg
   794-798    _claude_chat_sync_metered
 10179-10186  _client_ip
 26092-26119  _clip_prune
 26122-26132  _clip_recfile_for
 26648-26654  _clip_should_velocity
 26173-26255  _clip_to_discord
  3603-3612   _close_ai_session
 27172-27187  _cohost_broadcast
 27154-27158  _cohost_cfg
 27213-27225  _cohost_fire_highlight
 27161-27169  _cohost_gate
 27190-27210  _cohost_highlight
 26304-26338  _community_events_loop
 10798-10800  _conv_messages
  6942-6985   _cookie_alarm_loop
  1888-1892   _cookie_autorefresh_info
  1793-1797   _cookie_header
 13568-13600  _cpu_load_snapshot
  3913-3925   _create_index_safe
 23011-23117  _crowdsec_status
 22977-23008  _crowdsec_via_lapi
 22842-22860  _cscli_bin
 22866-22879  _cscli_path
  6832-6857   _daily_summary_loop
 22897-22914  _darf_journal_lesen
 25541-25564  _db_maintenance_loop
  6801-6829   _db_vacuum_loop
 17922-17946  _detect_foreign_ad
  1374-1385   _diag_path_owner
 19317-19361  _director_finalize
 20128-20135  _director_for
 19266-19314  _director_mark
 26542-26577  _disc_automod_check
 26515-26521  _disc_state_get
 26524-26531  _disc_state_set
 23560-23573  _discord_guild_filesize_bytes
 23759-23768  _discord_invite
 26476-26512  _discord_live_thread
 19468-19480  _discord_notify
 23660-23685  _discord_ops_alert
 26374-26472  _discord_post_user
 23824-25526  _discord_run_once
 23698-23756  _discord_start
 26063-26069  _discord_stop
 23581-23583  _discord_upload_limit_label
 23576-23578  _discord_upload_limit_mb
  6860-6937   _disk_alarm_loop
 28579-28628  _disk_autoclean
 28631-28644  _disk_guard_loop
 28571-28576  _disk_pct
 15716-15718  _drawtext_chain
 14034-14036  _dump_all_threads
 11499-11563  _enrich_proxies_with_geo
  2033-2077   _ensure_cookie_file_netscape
 23771-23821  _ensure_discord_invite
 26269-26301  _ensure_error_channel
  8689-8692   _ensure_notify_topic
 11744-11781  _ensure_proxy_ready
  8643-8670   _ensure_topic
   652-654    _env_int
   657-659    _env_int_range
 26341-26371  _error_channel_loop
 19512-19525  _event_webhook
 15165-15178  _evolution_loop
  5951-5985   _extract_file_payload
  2165-2167   _extract_urls_from_streamurl_node
 22882-22889  _f2b_sudo_hint
 19548-19550  _faster_whisper_available
 17811-17823  _fetch_ldnoobw_de
 11388-11406  _fetch_proxy_list
 19962-19990  _fetch_tiktok_room_id
   728-731    _ff_cmd
 15879-15884  _find_chromium
  3136-3140   _find_external_recorder
  2170-2172   _find_stream_urls
 14542-14567  _fire_webhooks
  7721-7730   _fork_safe
   809-818    _freeai_chat_sync_metered
 22932-22974  _geo_lookup_ips
  3592-3601   _get_ai_session
  7555-7595   _get_live_info
  2706-2713   _get_resolve_semaphore
  7985-8351   _handle_single_tracking
 28423-28425  _hb
 28428-28445  _hb_while
 15417-15419  _highlight_cfg
 15422-15451  _highlight_observe
 15887-15892  _htmlov_screenshot_cmd
 19706-19716  _httpx_proxy
 14575-14587  _in_quiet_hours
 29458-29489  _install_fast_eventloop
 10045-10099  _install_fast_json
 14039-14055  _install_faulthandler
 20824-20833  _intel_ensure_schema
 20871-20906  _intel_index_loop
 20845-20855  _intel_index_one
 20836-20842  _intel_semantic
  5320-5329   _is_authorized
  7886-7892   _is_dead
  2155-2157   _is_hevc
 22917-22923  _is_private_ip
  1538-1545   _is_process_running
  6539-6550   _is_quiet_hours
  1175-1184   _is_upload_window
 10134-10147  _json_error_handler
  6759-6789   _kick_broadcaster_id
 12074-12093  _kick_channel_live
  6673-6715   _kick_follower_count
 12686-12699  _kick_oauth_exchange
 12702-12704  _kick_oauth_page
 12645-12649  _kick_redirect_public
 12640-12642  _kick_redirect_source
 12632-12637  _kick_redirect_uri
  6658-6660   _kick_slug
 12652-12683  _kick_user_token
  3962-3965   _kind_from_filename
 14604-14609  _latest_popularity
 17833-17839  _learned_load
 17830-17831  _learned_path
 17841-17849  _learned_save
 20343-20376  _live_react_loop
 20139-20332  _live_react_worker
 18929-18940  _live_transcript_push
 20334-20341  _live_users
 19364-19408  _living_title_loop
 17790-17798  _load_banned_words_file
  1714-1787   _load_cookies_dict
 25742-25814  _local_backup_scan
 10116-10130  _log_5xx
 16302-16314  _looks_like_codec_err
 16297-16299  _looks_like_source_expired
  7802-7832   _loop_fehler
 14059-14068  _loop_heartbeat
 28393-28420  _loop_lag_monitor
 14071-14139  _loop_watchdog_thread
 18809-18823  _loyalty_add
 18800-18806  _loyalty_get
 18826-18834  _loyalty_top
 14741-14743  _manual_donations_total
  7894-7895   _mark_dead
 12245-12261  _marketing_loop
 27075-27093  _maybe_handle_command
 28730-28754  _maybe_hype_clip
  3880-3903   _migrate_columns
 27352-27363  _mod_is_exempt
 27366-27371  _mod_warn_first
 27374-27377  _mod_warn_text
 15205-15213  _modlog
   928-930    _multistream_targets
  7733-7734   _nc_create_subprocess_exec
  7737-7738   _nc_create_subprocess_shell
 12497-12514  _news_loop
 15243-15245  _normalize_ingest
  2347-2364   _note_check_duration
  8683-8686   _notify_topic_name
 12596-12607  _oauth_redirect_env
 12623-12629  _oauth_redirect_source
 12610-12620  _oauth_redirect_uri
 18955-18963  _oracle_memories
 19221-19255  _oracle_memorize
 18966-18979  _oracle_persona
 18948-18952  _oracle_recent_text
 15542-15550  _ov_atomic_write
 15530-15536  _ov_bar
 17746-17758  _ov_clip_text
 15539-15540  _ov_oneline
 22332-22361  _overlay_push
 15833-15876  _overlay_render_size
 15304-15308  _overlay_session_reset
 22284-22287  _overlay_src_ok
 17909-17919  _own_invites
 15828-15830  _parse_size
 23125-23205  _parse_ssh_attacks
  7157-7190   _pause_resume_cmd
  1842-1886   _persist_refreshed_cookies
  1680-1712   _pick_checked_pull_proxy
 10215-10228  _pin_auth_value
 10274-10275  _pin_clear_fail
 10254-10257  _pin_locked
 10260-10271  _pin_note_fail
 10231-10251  _pin_ok
 22174-22176  _piper_available
 22139-22161  _piper_list_voices
 22181-22206  _piper_pick_model
 22218-22265  _piper_say
 22132-22136  _piper_voice_roots
 14504-14539  _post_json_threaded
 15807-15825  _probe_video_size
  1566-1583   _proc_is_recorder
 11486-11497  _proxy_geo_cache_put
 11713-11741  _proxy_pool_refresh_loop
  1646-1677   _proxy_report_recording
 14024-14026  _prune_stall_dumps
 12555-12593  _public_base_url
 12315-12436  _public_stats
 19483-19509  _push_notify
 10376-10378  _pwa_dir
 11457-11472  _quick_validate_proxy
 14570-14572  _quiet_hours_config
 10341-10374  _rate_guard
 18774-18780  _react_warn
  7641-7680   _reap_proc
  2387-2409   _record_check_outcome
   723-725    _redact_stream_urls
 11640-11710  _refresh_proxy_pool
 22164-22170  _resolve_piper_model
  2181-2271   _resolve_via_html
  2529-2683   _resolve_via_webcast_api_v2
  2746-2808   _resolve_via_ytdlp
 26694-26823  _resolve_youtube_ingest
 20415-20422  _restream_active_platforms
 15289-15300  _restream_active_sources
 19993-20092  _restream_chat_guardian
 15454-15526  _restream_chat_push
 15216-15228  _restream_enabled
 15895-15982  _restream_html_overlay_start
 15985-15998  _restream_html_overlay_stop
  1123-1125   _restream_layout_mode
 15254-15277  _restream_overlay_files
 20380-20412  _restream_platform_state
 20543-20578  _restream_resume_after_restart
 16046-16104  _restream_tts_enqueue_wav
 15769-15801  _restream_tts_feeder
 15766-15767  _restream_tts_fifo_path
 16001-16028  _restream_tts_start
 16030-16044  _restream_tts_stop
 20425-20540  _restream_verify_loop
 25707-25719  _retention_loop
 25666-25704  _retention_scan
  2491-2493   _room_is_abo
  5989-6106   _run_ai_call
 14162-14175  _run_async_from_flask
 22926-22929  _run_priv
 29446-29454  _run_selfcheck_and_exit
 25722-25733  _s3_client
  7921-7972   _safe_send
  4584-4600   _sample_net_throughput
 17800-17808  _save_banned_words_file
  2439-2466   _schedule_next_check
 25620-25663  _scheduler_loop
  3906-3910   _schema_pk
 14179-14184  _scraper_session
 27380-27419  _screen_full
 12982-13019  _sec_headers
  2160-2162   _select_stream_from_data_section
 29259-29443  _selfcheck
  8695-8729   _send_live_notice
  1198-1202   _should_defer_upload
 26135-26170  _shrink_for_discord
 10381-10393  _sicheres_ziel
 28651-28668  _sign_health_check
 28671-28690  _sign_health_loop
  7750-7761   _spawn
  7764-7794   _spawn_from_flask
 23249-23252  _st_befund
 19718-19959  _start_chat_listener
 14142-14159  _start_loop_watchdog
 12460-12488  _stats_loop
 12439-12442  _stats_output_path
 12445-12457  _stats_write
  8423-8439   _storage_cleanup_loop
 28710-28717  _story_for
  3198-3204   _stream_url_expiry
  3213-3219   _stream_url_is_fresh
  3206-3211   _stream_url_ttl
 17873-17880  _streamer_persona_get
 17855-17861  _streamer_personas_load
 17852-17853  _streamer_personas_path
 17863-17871  _streamer_personas_save
 15721-15725  _studio_chain
 25839-25961  _system_backup
 25964-25994  _system_backup_loop
 11409-11448  _test_proxy
 12115-12124  _testpush_cfg
 12127-12144  _testpush_exec
 12096-12112  _testpush_resolve_live
  7897-7918   _tg_sprache_setzen
  8602-8612   _tg_topics_load_into_mem
  8599-8600   _tg_topics_path
  8614-8621   _tg_topics_save
 10189-10197  _token_ok
  8624-8628   _topic_forget
 14590-14601  _tracking_max_duration
  4171-4185   _tracking_remove_cleanup
  4202-4214   _tracking_resume_cleanup
  1432-1455   _try_attach_file_handler
 22208-22216  _tts_cleanup
 12052-12056  _tunnel_effective
 21634-21687  _twitch_channel_status
 27422-27565  _twitch_chat_loop
 27236-27339  _twitch_eventsub_loop
 15071-15074  _twitch_oauth_page
  1221-1234   _upload_queue_add
  1245-1247   _upload_queue_count
  1204-1213   _upload_queue_load
  1194-1196   _upload_queue_path
  1236-1243   _upload_queue_remove
  1215-1219   _upload_queue_save
  1249-1290   _upload_window_loop
  7614-7621   _uptime_s
 15231-15240  _url_host
   703-720    _url_ohne_zugang
   787-791    _usage_record_claude
  7835-7879   _verbindung_verloren
  6718-6749   _viewer_sample_loop
  6791-6798   _viewer_stats
 10278-10281  _wants_html
  7624-7638   _warn_empty_env
 28466-28561  _watchdog_loop
 26977-26985  _wchat_thank_ok
 19552-19582  _whisper_get_model
  7711-7718   _whisper_native_section
 18761-18767  _whisper_pool
 19651-19680  _whisper_segments
 19584-19648  _whisper_transcribe
 15552-15714  _write_restream_overlay
 27593-27672  _youtube_api_chat_loop
 21690-21793  _youtube_api_status
 21796-21863  _youtube_channel_status
 27675-27835  _youtube_chat_loop
 26829-26842  _youtube_restream_autoconfig
 26845-26869  _youtube_restream_autoconfig_inner
 26935-26963  _youtube_send
 21968-22009  _youtube_set_channel
 26872-26906  _yt_access_token
 26909-26924  _yt_live_chat_id
 27586-27590  _yt_oauth_configured
 26930-26932  _yt_sendrate_cfg
 27568-27583  _yt_timeout
  2730-2731   _ytdlp_detect_available
  2733-2744   _ytdlp_note_result
 14029-14031  _zombie_child_count
  7491-7515   about
  4081-4085   add_ai_log_entry
  3998-4001   add_archive_entry
  4697-4712   add_archive_rule
  4373-4407   add_recording
  4146-4163   add_tracking
  6109-6142   ai
  3745-3784   ai_chat
  3818-3828   ai_history_append
  3830-3835   ai_history_clear
  3807-3816   ai_history_load
  3792-3805   ai_rate_limit_check
  6171-6179   aireset
 19092-19111  azrael_chat
 27840-27962  brain_cmd
  3222-3406   build_recording_cmd
  4166-4169   bulk_add_trackings
  6988-7047   bulkadd
  8442-8582   check_all_trackings
  4218-4230   claim_live_transition
 17949-18704  class KickModerator
 16317-17633  class RestreamManager
 11826-11868  classify_proxy_anonymity
  6217-6415   cleanup
  5180-5221   cleanup_old_recordings
  4364-4371   clear_recording
 26580-26645  clip_moment
  4528-4577   compute_storage_forecast
  7110-7154   cookies_cmd
  4137-4143   count_trackings_for_chat
  4068-4079   decide_preferred_recorder
  4008-4011   delete_archive_entry
  4714-4722   delete_archive_rule
  5646-5793   diag
 28074-28135  einnahmen_cmd
  4522-4525   find_recordings_by_fingerprint
  4029-4045   finish_recording_attempt
  4190-4192   get_all_active_trackings
  4096-4099   get_all_checks
  4409-4412   get_all_recordings
  4471-4473   get_all_tags_with_counts
  4499-4502   get_annotations_for_recording
  4003-4006   get_archive_entry
  4492-4495   get_bookmarked_recordings
  1909-2026   get_cookie_health
  4459-4465   get_event_log
  4052-4066   get_last_recording_attempt
  2811-2916   get_live_status
  4980-4983   get_manual_recordings
  4507-4510   get_or_compute_inspect_sync
  5256-5300   get_outcome_breakdown
  4478-4481   get_priority_poll_interval
  4675-4684   get_profile_snapshots
  4047-4050   get_recent_recording_attempts
  4414-4417   get_recording_by_id
  4485-4488   get_recording_note
  3540-3563   get_redis
  4126-4129   get_stats
  5147-5178   get_storage_stats
  4815-4817   get_tiktok_status_distribution
  4232-4241   get_tracking_state
  4187-4188   get_trackings_for_group
  4996-4999   get_trash_recordings
  9350-10013  handle_recording_finished
  3928-3953   init_db
  5070-5124   inspect_stream_url
 22327-22329  is_revenue_platform
  4687-4695   list_archive_rules
  5450-5488   live
  7975-7983   live_check_worker
  3615-3649   llm_chat
  3672-3700   llm_chat_sync
  3657-3669   llm_list_models
  4425-4451   log_event
  1500-1533   log_recording_failure
  7304-7353   logs_cmd
 28758-29249  main
  6145-6168   on_ai_media
  7430-7456   on_ai_reply
  7459-7488   on_azrael_mention
  7520-7550   on_callback
 19114-19218  oracle_handle
  7193-7196   pause_tracking
  5310-5315   profile_keyboard
  7255-7301   quota
  8353-8420   reaper_loop
  4811-4813   record_tiktok_status
  6184-6214   recstatus
  3565-3573   redis_get_json
  3575-3581   redis_set_json
 28138-28148  report_cmd
 11871-11873  report_proxy_result
  2274-2301   resolve_tiktok_live_stream
  4991-4994   restore_recording
  7199-7202   resume_tracking
  4725-4805   run_archive_rules
 28151-28373  run_bot
 13951-13998  run_flask
  4603-4648   sample_bandwidth_for_active
  4654-4673   save_profile_snapshot
  4088-4094   save_tiktok_check
  4356-4362   set_recording_file
  4195-4199   set_tracking_paused
  4986-4989   soft_delete_recording
  8735-9348   split_and_send_video
  5363-5405   start
  4013-4027   start_recording_attempt
  6418-6456   stats
  4961-4978   stop_manual_recording
  7205-7252   stoprec
  6643-6651   summary_cmd
  7356-7427   sysres
  5795-5939   teststream
  5407-5448   tiktok
  7050-7107   topusers
  5525-5582   track
  5490-5522   track_exact
  5596-5644   tracklist
  4827-4959   trigger_manual_recording
  4317-4354   try_acquire_recording_lock
  5002-5061   universal_search
  5584-5594   untrack
 27965-28071  update_cmd
  4517-4520   update_recording_fingerprint
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
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
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
tiktokcheck.py         account_exists, configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
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
